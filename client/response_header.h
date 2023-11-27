#ifndef RESPONSE_HEADER_H_
#define RESPONSE_HEADER_H_

#include <cstdint>

class Header {};

class ResponseHeader : public Header {
public:
  ResponseHeader(uint8_t version, uint16_t code, uint32_t payload_size);
  uint8_t get_version();
  uint16_t get_code();
  uint32_t get_payload_size();
  
private:
  uint8_t version;
  uint16_t code;
  uint32_t payload_size;
};

#endif //RESPONSE_HEADER_H_