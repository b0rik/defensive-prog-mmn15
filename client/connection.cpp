#include <boost/asio.hpp>
#include <vector>
#include "connection.h"
#include <iostream>
#include <iomanip>

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

void Connection::write(std::vector<uint8_t> request_in_bytes) {
  int total_bytes_written = 0;

  while(total_bytes_written < request_in_bytes.size()) {
    size_t bytes_written = boost::asio::write(this->socket, boost::asio::buffer(request_in_bytes));
    total_bytes_written += bytes_written;
  }
}

std::vector<uint8_t> Connection::read() {
  std::vector<uint8_t> header;
  header.resize(7);
  boost::asio::read(this->socket, boost::asio::buffer(header));

  for (const auto& byte : header) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)byte << " ";
  }

  return header;
}