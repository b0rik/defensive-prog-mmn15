#ifndef CLIENT_H_
#define CLIENT_H_

#include <boost/asio.hpp>
#include <string>
#include <vector>

class Client {
public:
  Client(boost::asio::io_context& io_context, const std::string& address, const std::string& port);
  void connect(); // add error handling maybe error return value
  void send(std::vector<uint8_t> request_in_bytes); // add error handling
  std::vector<uint8_t> receive(); // add error handling
private:
  boost::asio::io_context& io_context;
  boost::asio::ip::tcp::socket socket;
  const std::string address;
  const std::string port;
};

#endif //CLIENT_H_