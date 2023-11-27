#ifndef REQUEST_PAYLOAD_H_
#define REQUEST_PAYLOAD_H_

#include <string>
#include <cstdint>

class Payload {
public:
  virtual uint32_t get_size() = 0;
};

class RequestUserPayload : public Payload {
public:
  RequestUserPayload(std::string name);
  std::string get_name();
  uint32_t get_size();

private:
  char name[255];
};

class RequestFilePayload : public Payload{
public:
  RequestFilePayload(std::string file_name);
  std::string get_file_name();
  uint32_t get_size();


private:
  char file_name[255];
};

class RequestPublicKeyPayload : public RequestUserPayload {
public: 
  RequestPublicKeyPayload(std::string name, std::string public_key);
  std::string get_public_key();
  uint32_t get_size();

private:
  char public_key[160]; // 160 bytes 
};

class RequestSentFilePayload : public RequestFilePayload{
public:
  RequestSentFilePayload(std::string file_name, uint32_t content_size, std::string message_content);
  uint32_t get_content_size();
  std::string get_message_content();
  uint32_t get_size();


private:
  uint32_t content_size;
  std::string message_content; // type?
};

#endif //REQUEST_PAYLOAD_H_

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