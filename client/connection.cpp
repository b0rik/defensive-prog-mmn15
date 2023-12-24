#include <boost/asio.hpp>
#include "connection.h"
#include "message.h"
#include "utils.h"

Connection::Connection(boost::asio::io_context& io_context, const std::string& address, const std::string& port)
    : io_context(io_context)
    , socket(io_context)
    , address(address)
    , port(port)
{}

void Connection::connect() {
    try {
        boost::asio::ip::tcp::resolver resolver(this->io_context);
        boost::asio::ip::tcp::resolver::results_type endpoint = resolver.resolve(this->address, this->port);
        boost::asio::connect(this->socket, endpoint);
    }
    catch (...) {
        // fail to connect
        throw std::exception("failed to connect.");
    }
}

void Connection::disconnect() {
    this->socket.close();
}

void Connection::send(const Message& message) {
    try {
        // write header
        boost::asio::write(this->socket, boost::asio::buffer(&message.header, sizeof(MessageHeader)));
        // write payload
        boost::asio::write(this->socket, boost::asio::buffer(message.payload.data(), message.payload.size()));
    }
    catch (...) {
        // error writing to server
        throw std::exception("failed to send to the server.");
    }
}

void Connection::receive(Message& message) {
    try {
        // read header
        boost::asio::read(this->socket, boost::asio::buffer(&(message.header.version), sizeof(MessageHeader) - CLIENT_ID_SIZE));
        message.header.version = utils::to_local_endian(message.header.version);
        message.header.code = utils::to_local_endian(message.header.code);
        message.header.payload_size = utils::to_local_endian(message.header.payload_size);
        // read payload
        message.payload.resize(message.header.payload_size);
        boost::asio::read(this->socket, boost::asio::buffer(message.payload.data(), message.payload.size()));
    }
    catch (const std::exception&) {
        // error reading from server
        throw std::exception("failed to read from the server");
    }
}