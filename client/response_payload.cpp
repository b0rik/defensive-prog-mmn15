#include <cstring>
#include "response_payload.h"

ResponseEmptyPayload::ResponseEmptyPayload() : size(0) {}

uint32_t ResponseEmptyPayload::get_size() {
  return size;
}

ResponsePayload::ResponsePayload(std::string client_id) {
  strncpy(this->client_id, client_id.c_str(), 16);
}

std::string ResponsePayload::get_client_id() {
  return std::string(this->client_id);
}

ResponseKeyPayload::ResponseKeyPayload(std::string client_id, std::string encrypted_key) 
  : ResponsePayload(client_id) 
  , encrypted_key(encrypted_key) {}

std::string ResponseKeyPayload::get_encrypted_key() {
  return encrypted_key;
}

ResponseReceiveFilePayload::ResponseReceiveFilePayload(std::string client_id, uint32_t content_size, std::string file_name, uint32_t cksum) 
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

