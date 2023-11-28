#include "client.h"

Client::Client(boost::asio::io_context& io_context, const std::string& address, const std::string& port)
  : io_context(io_context)
  , socket(io_context)
  , address(address)
  , port(port) {}

void Client::connect() {
  boost::asio::ip::tcp::resolver resolver(this->io_context);
  boost::asio::ip::tcp::resolver::results_type endpoint = resolver.resolve(this->address, this->port);
  boost::asio::connect(this->socket, endpoint);
}