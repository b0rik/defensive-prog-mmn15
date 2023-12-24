#include <iostream>
#include "session.h"
#include "file_wrapper.h"

Session::Session() 
    : id(DEFAULT_ID)
    , tries(0)
    , is_done(false) 
{
    try {
        process_info_file();
        process_user_file();
        process_key_file();
    }
    catch (std::exception& e) {
    // error
        std::cout << e.what() << std::endl;
        throw std::exception("failed to initialize session.");
    }
}

std::string Session::get_file_name() const { return this->file_name; }
std::string Session::get_address() const { return this->address; }
std::string Session::get_port() const { return this->port; }
std::string Session::get_name() const { return this->name; }
std::string Session::get_id() const { return this->id; }
std::string Session::get_public_rsa_key() const { return this->public_rsa_key; }
std::string Session::get_private_rsa_key() const { return this->private_rsa_key; }
std::string Session::get_aes_key() const { return this->aes_key; }
uint8_t Session::get_tries() const { return this->tries; }
uint32_t Session::get_cksum() const { return this->cksum; }
uint16_t Session::get_request_code() const { return this->request_code; }

void Session::set_id(const std::string id) { this->id = id; }
void Session::set_public_rsa_key(const std::string public_rsa_key) { this->public_rsa_key = public_rsa_key; }
void Session::set_private_rsa_key(const std::string private_rsa_key) { this->private_rsa_key = private_rsa_key; }
void Session::set_aes_key(const std::string aes_key) { this->aes_key = aes_key; }
void Session::set_cksum(const uint32_t cksum) { this->cksum = cksum; }
void Session::set_request_code(const uint16_t request_code) { this->request_code = request_code; }

bool Session::get_user_exists() const { return this->user_exists; }
void Session::reset_tries() { this->tries = 0; }
void Session::increment_tries() { this->tries++; }
bool Session::get_is_done() const { return this->is_done; }
void Session::done() { this->is_done = true; }

void Session::process_info_file() {
    // proccess info file
    try {
        // read address and port
        std::string full_address = file_wrapper::get_line_from_file(FULL_ADDRESS_LINE, INFO_FILE);
        size_t colon_index = full_address.find(':');
        if (colon_index >= 0) {
            this->address = full_address.substr(0, colon_index);
            this->port = full_address.substr(colon_index + 1);
        }
        else {
            throw std::exception("bad ip format. excpected <address:port>");
        }

        // read name
        this->name = file_wrapper::get_line_from_file(INFO_NAME_LINE, INFO_FILE);
        if (name.empty()) {
            throw std::exception("no name provided.");
        }

        // read file_name
        this->file_name = file_wrapper::get_line_from_file(FILE_NAME_LINE, INFO_FILE);
        if (file_name.empty()) {
            throw std::exception("no file name provided.");
        }
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
        throw std::exception(std::string("failed to process info file: " + INFO_FILE).c_str());

    }
}

void Session::process_user_file() {
    // proccess user file
    if(file_wrapper::file_exists(USER_FILE)) {
        this->user_exists = true;

        try {
            std::string name = file_wrapper::get_line_from_file(USER_NAME_LINE, USER_FILE);
            if (name.empty()) {
                throw std::exception("name not provided in user file.");
            }

            if (name != this->name) {
                throw std::exception("name in user file doesnt match name in info file.");
            }

            this->id = file_wrapper::get_line_from_file(ID_LINE, USER_FILE);
            if (id.empty()) {
                throw std::exception("id not provided in user file.");
            }

            size_t hex_id_size = CLIENT_ID_SIZE * 2;
            
            if (id.size() != hex_id_size) {
                throw std::exception(std::string("wrong size id. expected size " + hex_id_size).c_str());
            }

            std::string private_rsa_key = file_wrapper::get_file_from_line(USER_FILE, PRIVATE_RSA_KEY_LINE);
            if (private_rsa_key.empty()) {
                throw std::exception("private rsa key not provided in user file.");
            }

            this->private_rsa_key = private_rsa_key;

        }
        catch (std::exception& e) {
            std::cout << e.what() << std::endl;
            throw std::exception(std::string("failed to process user file: " + USER_FILE).c_str());
        }
    }
    else {
        this->user_exists = false;
    }
}

void Session::process_key_file() {
    if (file_wrapper::file_exists(KEY_FILE)) {
        try {
            std::string file_content;
            file_content = file_wrapper::get_file_from_line(KEY_FILE, 1);
            if (file_content.empty()) {
                throw std::exception("no key provided in key file");
            }

            if (file_content != this->get_private_rsa_key()) {
                throw std::exception("key in key file doesnt match key in user file.");
            }

            this->private_rsa_key = file_content;
        }
        catch (std::exception& e) {
            std::cout << e.what() << std::endl;
            throw std::exception(std::string("failed to process key file: " + KEY_FILE).c_str());
        }
    }
}