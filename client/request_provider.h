#pragma once
#include <cstdint>
#include "session.h"
#include "message.h"

const uint8_t VERSION = 3;

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