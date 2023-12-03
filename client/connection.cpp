#include <boost/asio.hpp>
#include <vector>
#include "connection.h"
#include <iostream>
#include <iomanip>
#include "message.h"

Connection::Connection(boost::asio::io_context& io_context, const std::string& address, const std::string& port)
  : io_context(io_context)
  , socket(io_context)
  , address(address)
  , port(port) {}

void Connection::connect() {
  boost::asio::ip::tcp::resolver resolver(this->io_context);
  boost::asio::ip::tcp::resolver::results_type endpoint = resolver.resolve(this->address, this->port);
  boost::asio::connect(this->socket, endpoint);
}

void Connection::write(Message& message) {
  boost::asio::write(this->socket, boost::asio::buffer(&message.header, sizeof(MessageHeader)));
  boost::asio::write(this->socket, boost::asio::buffer(message.payload.data(), message.payload.size()));
}

Message Connection::read() {
  Message message;
  std::vector<uint8_t> buffer;

  boost::asio::read(this->socket, boost::asio::buffer(&message.header, sizeof(MessageHeader)));
  message.payload.resize(message.header.payload_size);
  boost::asio::read(this->socket, boost::asio::buffer(message.payload.data(), message.payload.size()));

  return message;
}