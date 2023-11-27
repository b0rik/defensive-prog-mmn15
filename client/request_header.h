#ifndef REQUEST_HEADER_H_
#define REQUEST_HEADER_H_

#include <string>
#include <cstdint>
#include "response_header.h"

class RequestHeader : public ResponseHeader {
public:
  RequestHeader(std::string client_id, uint8_t version, uint16_t code, uint32_t payload_size);

private:
  char client_id[16];
};

#endif //REQUEST_HEADER_H_