// #include <cstring>
// #include <vector>
// #include "header.h"
// #include "serializer.h"

// Header::Header(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size) 
//   : version(version)
//   , code(code)
//   , payload_size(payload_size) {}

// uint8_t Header::get_version() {
//   return this->version;
// }

// uint16_t Header::get_code() {
//   return this->code;
// }

// uint32_t Header::get_payload_size() {
//   return this->payload_size;
// }

// std::vector<uint8_t> Header::serialize(Serializer serializer) {
//   std::vector<uint8_t> version_bytes;
//   serializer.serialize(version_bytes, this->version);
  
//   std::vector<uint8_t> code_bytes;
//   serializer.serialize(code_bytes, this->code);

//   std::vector<uint8_t> payload_size;
//   serializer.serialize(payload_size, this->payload_size);

//   std::vector<uint8_t> result;
//   result.insert(result.end(), version_bytes.begin(), version_bytes.end());
//   result.insert(result.end(), code_bytes.begin(), code_bytes.end());
//   result.insert(result.end(), payload_size.begin(), payload_size.end());

//   return result;
// }

// ResponseHeader::ResponseHeader(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size) : Header(version, code, payload_size) {}

// std::vector<uint8_t> ResponseHeader::to_bytes() {
//   std::vector<uint8_t> bytes = Header::to_bytes();
//   return bytes;  
// }

// RequestHeader::RequestHeader(const std::string& client_id, const  uint8_t& version, const uint16_t& code, const uint32_t& payload_size) 
//   : Header(version, code, payload_size) {
//   strncpy(this->client_id, client_id.c_str(), 16);
// }

// std::string RequestHeader::get_client_id() {
//   return std::string(this->client_id);
// }

// std::vector<uint8_t> RequestHeader::to_bytes() {
//   std::vector<uint8_t> bytes;
//   serialize_member(bytes, this->client_id);
//   std::vector<uint8_t> header_bytes = Header::to_bytes();
//   bytes.insert(bytes.end(), header_bytes.begin(), header_bytes.end());
//   return bytes;
// }

