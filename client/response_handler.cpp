#include <string>
#include "response_handler.h"
#include "session.h"
#include "utils.h"
#include "message.h"
#include "cryptopp_wrapper/RSAWrapper.h"
#include "cryptopp_wrapper/Base64Wrapper.h"
#include "file_wrapper.h"

ResponseHandler::ResponseHandler(Session& session) : session(session) {}

void ResponseHandler::handle(Message& response) {
    switch (utils::to_local_endian(response.header.code)) {
        case 2100: 
            handle_success_register(response);
            break;
        case 2101:
            handle_fail_register(response);
            break;
        case 2102:
        case 2105: 
            handle_aes_key(response);
            break;
        case 2103:
            handle_crc(response);
            break;
        case 2104:
            handle_ok(response);
            break;
        case 2106:
            handle_fail_login(response);
            break;
        case 2107:
            handle_server_error(response);
            break;
    }
}

void ResponseHandler::handle_success_register(Message& response) {
    // get id from response
    std::string id(CLIENT_ID_SIZE, '\0');
    response >> id;
    std::string hex_id = utils::bytes_to_hex_string(id);
    this->session.set_id(hex_id);

    // save id to file
    try {
        file_wrapper::reset_file(USER_FILE);
        file_wrapper::add_to_file(USER_FILE, this->session.get_name());
        file_wrapper::add_to_file(USER_FILE, hex_id);
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
        throw std::exception("failed to save user info to user file.");
    }

    this->session.reset_tries();

    this->session.set_request_code(1026);
}

void ResponseHandler::handle_fail_register(Message& response) {
    // terminate
    throw std::exception("failed to register.");
}

void ResponseHandler::handle_aes_key(Message& response) {
    // get encrypted aes key from response
    size_t payload_size = utils::to_local_endian(response.header.payload_size);
    size_t key_size = payload_size - CLIENT_ID_SIZE;
    std::string encrypted_aes_key(key_size, '\0');
    response >> encrypted_aes_key;

    // decrypt aes key
    try {
        RSAPrivateWrapper rsapriv(Base64Wrapper::decode(this->session.get_private_rsa_key()));
        std::string decrypted_aes_key = rsapriv.decrypt(encrypted_aes_key);
        this->session.set_aes_key(decrypted_aes_key);
    }
    catch (...) {
    // fail decrypt aes key
        if (this->session.get_tries() < MAX_TRIES) {
            this->session.increment_tries();
            return;
        }
        else {
            throw std::exception("failed to decrypt aes key.");
        }
    }

    this->session.reset_tries();

    this->session.set_request_code(1028);
}

void ResponseHandler::handle_crc(Message& response) {
    uint32_t cksum;
    response >> cksum;

    if (cksum == this->session.get_cksum()) {
        // 1029
        this->session.reset_tries();
        this->session.set_request_code(1029);
        return;
    }

    if (this->session.get_tries() < MAX_TRIES) {
        // 1030
        this->session.increment_tries();
        this->session.set_request_code(1030);
        return;
    }

    // 1031
    this->session.set_request_code(1031);
}

void ResponseHandler::handle_ok(Message& response) {
    // terminate
    throw std::exception("got ok from server.");
}

void ResponseHandler::handle_fail_login(Message& response) {
    this->session.reset_tries();
    this->session.set_request_code(1025);
}

void ResponseHandler::handle_server_error(Message& response) {
    if (this->session.get_tries() < MAX_TRIES) {
        std::cout << "Server responded with an error." << std::endl;
        this->session.increment_tries();
        return;
    }

    throw std::exception("server error.");
}
