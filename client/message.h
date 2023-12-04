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

#pragma pack(1)
struct MessageHeader {
  char client_id[16] = {0};
  uint8_t version;
  uint16_t code;
  uint32_t payload_size = 0;
};

#pragma pack(1)
struct Message {
  MessageHeader header{};
  vector<uint8_t> payload;

  template <typename T>
  friend Message& operator << (Message& message, const T& data) {
    size_t size = message.payload.size();
    message.payload.resize(size + sizeof(T));
    memcpy(message.payload.data() + size, &data, sizeof(T));

    message.header.payload_size = message.payload.size();
    
    return message;
  }

  template <typename T, size_t N>
  friend Message& operator << (Message& message, const T (&data)[N]) {
    size_t size = message.payload.size();
    message.payload.resize(size + N * sizeof(T));
    memcpy(message.payload.data() + size, data, N * sizeof(T));

    message.header.payload_size = message.payload.size();

    return message;
  }

  template <typename T>
  friend Message& operator >> (Message& message, T& data) {
    size_t size = message.payload.size() - sizeof(T);
    memcpy(&data, message.payload.data() + size, sizeof(T));
    message.payload.resize(size);

    message.header.payload_size = message.payload.size();
    
    return message;
  }
};

#endif // MESSAGE_H_