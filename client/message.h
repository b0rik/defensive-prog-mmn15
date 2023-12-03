#ifndef MESSAGE_H_
#define MESSAGE_H_

// #include <vector>
// #include "header.h"
// #include "payload.h"
// #include <vector>

// class Message {
// public:
//   Message(Header& header, Payload& payload);
//   Header& get_header();
//   Payload& get_payload();
//   std::vector<uint8_t> to_bytes();

// private:
//   Header& header;
//   Payload& payload;
// };

#include <vector>
#include <cstdint>

using namespace std;
struct MessageHeader {
  char client_id[16];
  uint8_t version;
  uint16_t code;
  uint32_t payload_size = 0;
};

struct Message {
  MessageHeader header{};
  vector<uint8_t> payload;

  template <typename T>
  friend Message& operator << (Message& message, const T& data) {
    size_t size = message.payload.size();
    message.body.resize(size + sizeof(T));
    memcpy(message.body.data() + size, &data, sizeof(T));

    message.header.payload_size = payload.size();
    
    return message;
  }

  template <typename T>
  friend Message& operator >> (Message& message, T& data) {
    size_t size = message.payload.size() - sizeof(T);
    memcpy(&data, message.body.data() + size, sizeof(T));
    message.body.resize(size);

    message.header.payload_size = payload.size();
    
    return message
  }
};

#endif // MESSAGE_H_