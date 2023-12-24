#pragma once
#include <cstdint>
#include "session.h"
#include "message.h"

const uint8_t VERSION = 3;
const size_t NAME_SIZE = 255;
const size_t PUBLIC_RSA_KEY_SIZE = 160;
const size_t FILE_NAME_SIZE = 255;

class RequestProvider {
public:
    RequestProvider(Session& session);
    void make_request(Message& request);

private:
    void make_name_request(Message& request);
    void make_key_request(Message& request);
    void make_file_request(Message& request);
    void make_crc_request(Message& request);

    Session& session;
};