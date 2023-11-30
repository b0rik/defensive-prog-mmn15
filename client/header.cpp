#include <cstring>
#include <vector>
#include "header.h"

template <typename T>
void serialize_member(std::vector<uint8_t>& result, const T& data) {
    const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&data);
    result.insert(result.end(), bytes, bytes + sizeof(T));
}

Header::Header(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size) 
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

std::vector<uint8_t> Header::to_bytes() {
  std::vector<uint8_t> bytes;
  serialize_member(bytes, this->version);
  serialize_member(bytes, this->code);
  serialize_member(bytes, this->payload_size);
  return bytes;
}

ResponseHeader::ResponseHeader(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size) : Header(version, code, payload_size) {}

std::vector<uint8_t> ResponseHeader::to_bytes() {
  std::vector<uint8_t> bytes = Header::to_bytes();
  return bytes;  
}

RequestHeader::RequestHeader(const std::string& client_id, const  uint8_t& version, const uint16_t& code, const uint32_t& payload_size) 
  : Header(version, code, payload_size) {
  strncpy(this->client_id, client_id.c_str(), 16);
}

std::string RequestHeader::get_client_id() {
  return std::string(this->client_id);
}

std::vector<uint8_t> RequestHeader::to_bytes() {
  std::vector<uint8_t> bytes;
  serialize_member(bytes, this->client_id);
  std::vector<uint8_t> header_bytes = Header::to_bytes();
  bytes.insert(bytes.end(), header_bytes.begin(), header_bytes.end());
  return bytes;
}

