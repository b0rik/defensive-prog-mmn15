#ifndef MESSAGE_H_
#define MESSAGE_H_

#include "header.h"
#include "payload.h"

class Message {
public:
  Message(const Header& header, const Payload& payload);
  const Header& get_header();
  const Payload& get_payload();

private:
  const Header& header;
  const Payload& payload;
};

#endif // MESSAGE_H_