#pragma once
#include <string>
#include <cstdint>
#include "message.h"

const size_t NAME_SIZE = 255;
const size_t PUBLIC_RSA_KEY_SIZE = 160;
const size_t FILE_NAME_SIZE = 255;

const std::string INFO_FILE = "transfer.info";
const std::string USER_FILE = "me.info";
const std::string KEY_FILE = "priv.key";

const size_t FULL_ADDRESS_LINE = 1;
const size_t INFO_NAME_LINE = 2;
const size_t FILE_NAME_LINE = 3;
const size_t USER_NAME_LINE = 1;
const size_t ID_LINE = 2;
const size_t PRIVATE_RSA_KEY_LINE = 3;

const size_t MAX_TRIES = 3;

const std::string DEFAULT_ID(CLIENT_ID_SIZE * 2, 'a');

class Session {	
public:
	Session();

	std::string get_file_name() const;
	std::string get_address() const;
	std::string get_port() const;
	std::string get_name() const;
	std::string get_id() const;
	std::string get_public_rsa_key() const;
	std::string get_private_rsa_key() const;
	std::string get_aes_key() const;
	uint8_t get_tries() const;
	uint32_t get_cksum() const;
	uint16_t get_request_code() const;
	bool get_is_done() const;
	bool get_user_exists() const;

	void set_id(const std::string id);
	void set_public_rsa_key(const std::string public_rsa_key);
	void set_private_rsa_key(const std::string private_rsa_key);
	void set_aes_key(const std::string aes_key);
	void set_cksum(const uint32_t cksum);
	void set_request_code(const uint16_t request_code);

	void reset_tries();
	void increment_tries();
	void done();


private:
	void process_info_file();
	void process_user_file();
	void process_key_file();

	std::string file_name;
	std::string name;
	std::string address;
	std::string port;
	std::string id; // in hex
	std::string public_rsa_key;
	std::string private_rsa_key; // in base64
	std::string aes_key;
	uint8_t tries;
	uint32_t cksum;
	uint16_t request_code;
	bool is_done;
	bool user_exists;
};
