#ifndef PAYLOAD_H_
#define PAYLOAD_H_

#include <string>
#include <cstdint>
#include <vector>

class Payload {
public:
  virtual std::vector<uint8_t> to_bytes() = 0;
};

class RequestUserPayload : public Payload {
public:
  RequestUserPayload(const std::string& name);
  std::string get_name();
  virtual std::vector<uint8_t> to_bytes();

private:
  char name[255];
};

class RequestFilePayload : public Payload{
public:
  RequestFilePayload(const std::string& file_name);
  std::string get_file_name();
  virtual std::vector<uint8_t> to_bytes();

private:
  char file_name[255];
};

class RequestPublicKeyPayload : public RequestUserPayload {
public: 
  RequestPublicKeyPayload(const std::string& name, const std::string& public_key);
  std::string get_public_key();
  std::vector<uint8_t> to_bytes();


private:
  char public_key[160]; // 160 bytes 
};

class RequestSentFilePayload : public RequestFilePayload{
public:
  RequestSentFilePayload(const std::string& file_name, const uint32_t& content_size, const std::string& message_content);
  uint32_t get_content_size();
  std::string get_message_content();
  std::vector<uint8_t> to_bytes();

private:
  const uint32_t content_size;
  const std::string message_content; // type?
};

class ResponseEmptyPayload : public Payload {
public:
  ResponseEmptyPayload();
  uint32_t get_size();
  virtual std::vector<uint8_t> to_bytes();


private:
  const uint32_t size;
};

class ResponsePayload : public ResponseEmptyPayload {
public:
  ResponsePayload(const std::string& client_id);
  std::string get_client_id();
  virtual std::vector<uint8_t> to_bytes();

private:
  char client_id[16];
};

class ResponseKeyPayload : public ResponsePayload {
public:
  ResponseKeyPayload(const std::string& client_id, const std::string& encrypted_key);
  std::string get_encrypted_key();
  std::vector<uint8_t> to_bytes();

private:
  const std::string encrypted_key; // type?
};

class ResponseReceiveFilePayload : public ResponsePayload {
public:
  ResponseReceiveFilePayload(const std::string& client_id, const uint32_t& content_size, const std::string& file_name, const uint32_t& cksum);
  uint32_t get_content_size();
  std::string get_file_name();
  uint32_t get_cksum();
  std::vector<uint8_t> to_bytes();

private:
  const uint32_t content_size;
  char file_name[255];
  const uint32_t cksum;
};

#endif //PAYLOAD_H_

