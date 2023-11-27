#include <cstring>
#include "request_header.h"

RequestHeader::RequestHeader(std::string client_id, uint8_t version, uint16_t code, uint32_t payload_size) 
  : ResponseHeader(version, code, payload_size) {
  strncpy(this->client_id, client_id.c_str(), 16);
}
