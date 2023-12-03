// #include <vector>
// #include "message.h"

// Message::Message(Header& header, Payload& payload) 
//   : header(header), payload(payload) {}

// Header& Message::get_header() {
//   return this->header;
// }

// Payload& Message::get_payload() {
//   return this->payload;
// }

// std::vector<uint8_t> Message::to_bytes() {
//   std::vector<uint8_t> bytes;

//   std::vector<uint8_t> header_bytes = this->header.to_bytes();
//   std::vector<uint8_t> payload_bytes = this->payload.to_bytes();

//   bytes.insert(bytes.end(), header_bytes.begin(), header_bytes.end());
//   bytes.insert(bytes.end(), payload_bytes.begin(), payload_bytes.end());
  
//   return bytes;
// }
