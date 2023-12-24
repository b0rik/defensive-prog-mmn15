#pragma once
#include <vector>
#include <string>
#include <cstdint>
#include "utils.h"

const size_t CLIENT_ID_SIZE = 16;

#pragma pack(push, 1)
struct MessageHeader {
    char client_id[CLIENT_ID_SIZE] = { 0 };
    uint8_t version;
    uint16_t code;
    uint32_t payload_size = 0;
};

struct Message {
    MessageHeader header;
    std::vector<uint8_t> payload;

    friend Message& operator << (Message& message, std::string& data) {
        size_t size = message.payload.size();
        message.payload.resize(size + data.size());
        memcpy(message.payload.data() + size, data.data(), data.size());

        message.header.payload_size = message.payload.size();

        return message;
    }

    template <typename T>
        friend Message& operator << (Message& message, const T& data) {
        size_t size = message.payload.size();
        T data_le = utils::to_little_endian(data);
        message.payload.resize(size + sizeof(T));
        memcpy(message.payload.data() + size, &data_le, sizeof(T));

        message.header.payload_size = message.payload.size();

        return message;
    }

    friend Message& operator >> (Message& message, std::string& data) {
        size_t size = message.payload.size() - data.size();
        memcpy(data.data(), message.payload.data() + size, data.size());
        message.payload.resize(size);

        message.header.payload_size = message.payload.size();

        return message;
    }

    template <typename T>
        friend Message& operator >> (Message& message, T& data) {
        size_t size = message.payload.size() - sizeof(T);
        T data_le;
        memcpy(&data_le, message.payload.data() + size, sizeof(T));
        message.payload.resize(size);
        data = utils::to_local_endian(data_le);

        message.header.payload_size = message.payload.size();

        return message;
    }
};
#pragma pack(pop)