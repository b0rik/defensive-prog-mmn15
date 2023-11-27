#include "response_header.h"

ResponseHeader::ResponseHeader(uint8_t version, uint16_t code, uint32_t payload_size) 
  : version(version)
  , code(code)
  , payload_size(payload_size) {}

uint8_t ResponseHeader::get_version() {
  return this->version;
}

uint16_t ResponseHeader::get_code() {
  return this->code;
}

uint32_t ResponseHeader::get_payload_size() {
  return this->payload_size;
}