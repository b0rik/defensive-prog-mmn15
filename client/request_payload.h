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