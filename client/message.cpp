#include "message.h"

Message::Message(const Header& header, const Payload& payload) 
  : header(header), payload(payload) {}

const Header& Message::get_header() {
  return this->header;
}

const Payload& Message::get_payload() {
  return this->payload;
}