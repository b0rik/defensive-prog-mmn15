#include <cstring>
#include "payload.h"

ResponseEmptyPayload::ResponseEmptyPayload() : size(0) {}

uint32_t ResponseEmptyPayload::get_size() {
  return size;
}

ResponsePayload::ResponsePayload(const std::string& client_id) {
  strncpy(this->client_id, client_id.c_str(), 16);
}

std::string ResponsePayload::get_client_id() {
  return std::string(this->client_id);
}

ResponseKeyPayload::ResponseKeyPayload(const std::string& client_id, const std::string& encrypted_key) 
  : ResponsePayload(client_id) 
  , encrypted_key(encrypted_key) {}

std::string ResponseKeyPayload::get_encrypted_key() {
  return encrypted_key;
}

ResponseReceiveFilePayload::ResponseReceiveFilePayload(const std::string& client_id, const uint32_t& content_size, const std::string& file_name, const uint32_t& cksum) 
  : ResponsePayload(client_id)
  , content_size(content_size)
  , cksum(cksum) {
  strncpy(this->file_name, file_name.c_str(), 255);
}

uint32_t ResponseReceiveFilePayload::get_content_size() {
  return content_size;
}

std::string ResponseReceiveFilePayload::get_file_name() {
  return std::string(this->file_name);
}

uint32_t ResponseReceiveFilePayload::get_cksum() {
  return cksum;
}

RequestUserPayload::RequestUserPayload(const std::string& name) {
  strncpy(this->name, name.c_str(), 255);
}

std::string RequestUserPayload::get_name() {
  return std::string(this->name);
}

RequestFilePayload::RequestFilePayload(const std::string& file_name) {
  strncpy(this->file_name, file_name.c_str(), 255);
}

std::string RequestFilePayload::get_file_name() {
  return std::string(this->file_name);
}

RequestPublicKeyPayload::RequestPublicKeyPayload(const std::string& name, const std::string& public_key) 
  : RequestUserPayload(name) {
    strncpy(this->public_key, public_key.c_str(), 160);
}

std::string RequestPublicKeyPayload::get_public_key() {
  return std::string(this->public_key);
}


RequestSentFilePayload::RequestSentFilePayload(const std::string& file_name, const uint32_t& content_size, const std::string& message_content)
  : RequestFilePayload(file_name)
  , content_size(content_size)
  , message_content(message_content) {}

uint32_t RequestSentFilePayload::get_content_size() {
  return this->content_size;
}

std::string RequestSentFilePayload::get_message_content() {
  return this->message_content;
}