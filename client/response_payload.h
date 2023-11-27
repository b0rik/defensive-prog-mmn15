#ifndef RESPONSE_PAYLOAD_H_
#define RESPONSE_PAYLOAD_H_

#include <string>
#include <cstdint>

class ResponseEmptyPayload {
public:
  ResponseEmptyPayload();
  uint32_t get_size();

private:
  uint32_t size;
};

class ResponsePayload : public ResponseEmptyPayload {
public:
  ResponsePayload(std::string client_id);
  std::string get_client_id();

private:
  char client_id[16];
};

class ResponseKeyPayload : public ResponsePayload {
public:
  ResponseKeyPayload(std::string client_id, std::string encrypted_key);
  std::string get_encrypted_key();

private:
  std::string encrypted_key; // type?
};

class ResponseReceiveFilePayload : public ResponsePayload {
public:
  ResponseReceiveFilePayload(std::string client_id, uint32_t content_size, std::string file_name, uint32_t cksum);
  uint32_t get_content_size();
  std::string get_file_name();
  uint32_t get_cksum();

private:
  uint32_t content_size;
  char file_name[255];
  uint32_t cksum;
};

#endif //RESPONSE_PAYLOAD_H_