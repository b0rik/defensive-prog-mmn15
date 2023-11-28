#ifndef HEADER_H_
#define HEADER_H_

#include <string>
#include <cstdint>

class Header {
public:
  Header(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size);
  uint8_t get_version();
  uint16_t get_code();
  uint32_t get_payload_size();
  
private:
  const uint8_t version;
  const uint16_t code;
  const uint32_t payload_size;
};

class ResponseHeader : public Header {
public:
  ResponseHeader(const uint8_t& version, const uint16_t& code, const uint32_t& payload_size);
};

class RequestHeader : public Header {
public:
  RequestHeader(const std::string& client_id, const uint8_t& version, const uint16_t& code, const uint32_t& payload_size);

private:
  char client_id[16];
};

#endif //HEADER_H_