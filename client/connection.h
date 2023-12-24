#pragma once
#include <boost/asio.hpp>
#include <string>
#include "message.h"

class Connection {
public:
    Connection(boost::asio::io_context& io_context, const std::string& address, const std::string& port);
    void connect();
    void disconnect();
    // send message
    void send(const Message& message); 
    // receive data into message
    void receive(Message& message);

private:
    boost::asio::io_context& io_context;
    boost::asio::ip::tcp::socket socket;
    const std::string address;
    const std::string port;
};

