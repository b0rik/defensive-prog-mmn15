#ifndef MESSAGE_H_
#define MESSAGE_H_

#include "response_header.h"
#include "response_payload.h"

class Message {
public:
  Message(Header& header, Payload& payload);
  ~Message();
  Header* get_header();
  Payload* get_payload();

private:
  Header& header;
  Payload& payload;
};

#endif // MESSAGE_H_