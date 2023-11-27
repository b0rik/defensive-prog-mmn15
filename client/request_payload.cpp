#include <cstring>
#include "request_payload.h"

RequestUserPayload::RequestUserPayload(std::string name) {
  strncpy(this->name, name.c_str(), 255);
}

std::string RequestUserPayload::get_name() {
  return std::string(this->name);
}

uint32_t RequestUserPayload::get_size() {
  return 255;
}

RequestFilePayload::RequestFilePayload(std::string file_name) {
  strncpy(this->file_name, file_name.c_str(), 255);
}

std::string RequestFilePayload::get_file_name() {
  return std::string(this->file_name);
}

uint32_t RequestFilePayload::get_size() {
  return 255;
}

RequestPublicKeyPayload::RequestPublicKeyPayload(std::string name, std::string public_key) 
  : RequestUserPayload(name) {
    strncpy(this->public_key, public_key.c_str(), 160);
}

std::string RequestPublicKeyPayload::get_public_key() {
  return std::string(this->public_key);
}

uint32_t RequestPublicKeyPayload::get_size() {
  return 250 + 160;
}

RequestSentFilePayload::RequestSentFilePayload(std::string file_name, uint32_t content_size, std::string message_content)
  : RequestFilePayload(file_name)
  , content_size(content_size)
  , message_content(message_content) {}

uint32_t RequestSentFilePayload::get_content_size() {
  return this->content_size;
}

std::string RequestSentFilePayload::get_message_content() {
  return this->message_content;
}

uint32_t RequestSentFilePayload::get_size() {
  return 255 + 4 + this->content_size;
}