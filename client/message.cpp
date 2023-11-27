#include "message.h"

Message::Message(Header& header, Payload& payload) 
  : header(header), payload(payload) {}

Message::~Message() {} // what to put here?

Header* Message::get_header() {
  return &this->header;
}

Payload* Message::get_payload() {
  return &this->payload;
}