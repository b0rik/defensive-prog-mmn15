#pragma once
#include <string>
#include <vector>
#include <iomanip>
#include <sstream>

namespace utils {
    inline std::string hex_string_to_bytes(const std::string hexString) {
        std::string bytes;
        for (size_t i = 0; i < hexString.length(); i += 2) {
            std::string byteString = hexString.substr(i, 2);
            uint8_t byte = static_cast<uint8_t>(std::stoi(byteString, nullptr, 16));
            bytes += byte;
        }
        return bytes;
    }

    inline bool is_big_endian() {
    uint16_t test = 1;
    return (*(reinterpret_cast<char*>(&test)) == 0);
    }

    inline std::string bytes_to_hex_string( const std::string& buffer) {
    std::ostringstream ret;
    for (size_t i = 0; i < buffer.size(); i++)
        ret << std::hex << std::setfill('0') << std::setw(2) << (0xFF & buffer[i]);
    return ret.str();
    }

    template <typename T>
    T to_local_endian(const T& num) {
    if (is_big_endian()) {
        T num_local;
        std::vector<uint8_t> num_bytes(sizeof(T));
        memcpy(num_bytes.data(), &num, sizeof(T));
        std::reverse(num_bytes.begin(), num_bytes.end());
        memcpy(&num_local, num_bytes.data(), num_bytes.size());
        return num_local;
    }

    return num;
    }

    template <typename T>
    T to_little_endian(const T& num) {
    if (is_big_endian()) {
        T num_le;
        std::vector<uint8_t> num_bytes(sizeof(T));
        memcpy(num_bytes.data(), &num, sizeof(T));
        std::reverse(num_bytes.begin(), num_bytes.end());
        memcpy(&num_le, num_bytes.data(), num_bytes.size());
        return num_le;
    }

    return num;
    }
}
