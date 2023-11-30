#include <cstring>
#include <vector>
#include "payload.h"

template <typename T>
void serialize_member(std::vector<uint8_t>& result, const T& data) {
    const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&data);
    result.insert(result.end(), bytes, bytes + sizeof(T));
}

ResponseEmptyPayload::ResponseEmptyPayload() : size(0) {}

uint32_t ResponseEmptyPayload::get_size() {
  return size;
}

std::vector<uint8_t> ResponseEmptyPayload::to_bytes() {
  std::vector<uint8_t> bytes;
  return bytes;
}

ResponsePayload::ResponsePayload(const std::string& client_id) {
  strncpy(this->client_id, client_id.c_str(), 16);
}

std::string ResponsePayload::get_client_id() {
  return std::string(this->client_id);
}

std::vector<uint8_t> ResponsePayload::to_bytes() {
  std::vector<uint8_t> bytes;
  serialize_member(bytes, this->client_id);
  return bytes;
}

ResponseKeyPayload::ResponseKeyPayload(const std::string& client_id, const std::string& encrypted_key) 
  : ResponsePayload(client_id) 
  , encrypted_key(encrypted_key) {}

std::string ResponseKeyPayload::get_encrypted_key() {
  return encrypted_key;
}

std::vector<uint8_t> ResponseKeyPayload::to_bytes() {
  std::vector<uint8_t> bytes = ResponsePayload::to_bytes();
  serialize_member(bytes, this->encrypted_key);
  return bytes;
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

std::vector<uint8_t> ResponseReceiveFilePayload::to_bytes() {
  std::vector<uint8_t> bytes = ResponsePayload::to_bytes();
  serialize_member(bytes, this->content_size);
  serialize_member(bytes, this->file_name);
  serialize_member(bytes, this->cksum);
  return bytes;
}

RequestUserPayload::RequestUserPayload(const std::string& name) {
  strncpy(this->name, name.c_str(), 255);
}

std::string RequestUserPayload::get_name() {
  return std::string(this->name);
}

std::vector<uint8_t> RequestUserPayload::to_bytes() {
  std::vector<uint8_t> bytes;
  serialize_member(bytes, this->name);
  return bytes;
}

RequestFilePayload::RequestFilePayload(const std::string& file_name) {
  strncpy(this->file_name, file_name.c_str(), 255);
}

std::string RequestFilePayload::get_file_name() {
  return std::string(this->file_name);
}

std::vector<uint8_t> RequestFilePayload::to_bytes() {
  std::vector<uint8_t> bytes;
  serialize_member(bytes, this->file_name);
  return bytes;
}

RequestPublicKeyPayload::RequestPublicKeyPayload(const std::string& name, const std::string& public_key) 
  : RequestUserPayload(name) {
    strncpy(this->public_key, public_key.c_str(), 160);
}

std::string RequestPublicKeyPayload::get_public_key() {
  return std::string(this->public_key);
}

std::vector<uint8_t> RequestPublicKeyPayload::to_bytes() {
  std::vector<uint8_t> bytes = RequestUserPayload::to_bytes();
  serialize_member(bytes, this->public_key);
  return bytes;
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

std::vector<uint8_t> RequestSentFilePayload::to_bytes() {
  std::vector<uint8_t> bytes = RequestFilePayload::to_bytes();
  serialize_member(bytes, this->content_size);
  serialize_member(bytes, this->message_content);
  return bytes;
}