#include <cstring>
#include "header.h"

Header::Header(uint8_t version, uint16_t code, uint32_t payload_size) 
  : version(version)
  , code(code)
  , payload_size(payload_size) {}

uint8_t Header::get_version() {
  return this->version;
}

uint16_t Header::get_code() {
  return this->code;
}

uint32_t Header::get_payload_size() {
  return this->payload_size;
}

ResponseHeader::ResponseHeader(uint8_t version, uint16_t code, uint32_t payload_size) : Header(version, code, payload_size) {}

RequestHeader::RequestHeader(std::string client_id, uint8_t version, uint16_t code, uint32_t payload_size) 
  : Header(version, code, payload_size) {
  strncpy(this->client_id, client_id.c_str(), 16);
}

