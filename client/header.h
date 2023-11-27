#ifndef HEADER_H_
#define HEADER_H_

#include <string>
#include <cstdint>

class Header {
public:
  Header(uint8_t version, uint16_t code, uint32_t payload_size);
  uint8_t get_version();
  uint16_t get_code();
  uint32_t get_payload_size();
  
private:
  uint8_t version;
  uint16_t code;
  uint32_t payload_size;
};

class ResponseHeader : public Header {
public:
  ResponseHeader(uint8_t version, uint16_t code, uint32_t payload_size);
};

class RequestHeader : public Header {
public:
  RequestHeader(std::string client_id, uint8_t version, uint16_t code, uint32_t payload_size);

private:
  char client_id[16];
};

#endif //HEADER_H_