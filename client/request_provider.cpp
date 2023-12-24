#include <string>
#include <cstdint>
#include "request_provider.h"
#include "message.h"
#include "utils.h"
#include "cryptopp_wrapper/Base64Wrapper.h"
#include "cryptopp_wrapper/AESWrapper.h"
#include "cryptopp_wrapper/RSAWrapper.h"
#include "file_wrapper.h"
#include "cksum.h"

RequestProvider::RequestProvider(Session& session) : session(session) {}

void RequestProvider::make_request(Message& request) {
    // header
    // id
    std::string client_id_hex = this->session.get_id();
    std::string client_id_bytes;
    client_id_bytes = utils::hex_string_to_bytes(client_id_hex);
    memcpy(request.header.client_id, client_id_bytes.data(), client_id_bytes.size());

    // version
    request.header.version = utils::to_little_endian(VERSION);

    // code
    request.header.code = utils::to_little_endian(this->session.get_request_code());

    // payload
    switch (utils::to_local_endian((request.header.code))) {
    case 1025: // register
    case 1027: // relogin
        make_name_request(request);
        break;
    case 1026: // public rsa key
        make_key_request(request);
        break;
    case 1028: // send file
        make_file_request(request);
        break;
    case 1029: // crc ok
    case 1030: // crc fail
    case 1031: // crc fail abort
        make_crc_request(request);
        break;
    }
}

void RequestProvider::make_name_request(Message& request) {
    std::string name(NAME_SIZE, '\0');
    memcpy(name.data(), this->session.get_name().data(), this->session.get_name().size());

    request << name;
}

void RequestProvider::make_key_request(Message& request) {
    make_name_request(request);

    // generate rsa pair
    RSAPrivateWrapper rsapriv;
    std::string privkey = rsapriv.getPrivateKey();
    std::string pubkey = rsapriv.getPublicKey();

    std::string base64privkey = Base64Wrapper::encode(privkey);
    this->session.set_private_rsa_key(base64privkey);
    this->session.set_public_rsa_key(pubkey);
    
    // save private key to files
    try {
        file_wrapper::add_to_file(USER_FILE, base64privkey);
        file_wrapper::reset_file(KEY_FILE);
        file_wrapper::add_to_file(KEY_FILE, base64privkey);
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
        throw std::exception("failed to save key to files.");
    }

    request << pubkey;
}

void RequestProvider::make_file_request(Message& request) {
    std::string file_name = this->session.get_file_name();
    std::string file_content;

    // get file content
    try {
        file_content = file_wrapper::get_file(file_name);
    }
    catch (std::exception& e) {
    // fail to get file
        std::cout << e.what() << std::endl;
        throw std::exception("failed to get file.");
    }

    // calculate cksum
    uint32_t cksum = memcrc((char*)file_content.data(), file_content.size());
    this->session.set_cksum(cksum);

    std::string encrypted_file;
    // encrypt file with aes key
    try {
        std::string aes_key = this->session.get_aes_key();
        AESWrapper aes((const unsigned char*)aes_key.data(), aes_key.size());
        encrypted_file = aes.encrypt((char*)file_content.data(), file_content.size());
    } 
    catch (...) {
    // fail to encrypt file
        throw std::exception("failed to encrypt file.");
    }

    // get content size
    uint32_t content_size = encrypted_file.size();

    request << content_size;
    make_crc_request(request);
    request << encrypted_file;
}

void RequestProvider::make_crc_request(Message& request) {
    std::string file_name(FILE_NAME_SIZE, '\0');
    memcpy(file_name.data(), this->session.get_file_name().data(), this->session.get_file_name().size());

    request << file_name;
}