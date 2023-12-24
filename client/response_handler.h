#pragma once
#include "session.h"
#include "message.h"

class ResponseHandler {
public:
    ResponseHandler(Session& session);
    void handle(Message& response);

private:
    void handle_success_register(Message& response);
    void handle_fail_register(Message& response);
    void handle_aes_key(Message& response);
    void handle_crc(Message& response);
    void handle_ok(Message& response);
    void handle_fail_login(Message& response);
    void handle_server_error(Message& response);

    Session& session;
};