#ifndef CONNECTION_H_
#define CONNECTION_H_

#include <boost/asio.hpp>
#include <string>
#include <vector>

class Connection {
public:
  Connection(boost::asio::io_context& io_context, const std::string& address, const std::string& port);
  void connect(); // add error handling maybe error return value
  void write(std::vector<uint8_t> request_in_bytes); // add error handling
  std::vector<uint8_t> read(); // add error handling
private:
  boost::asio::io_context& io_context;
  boost::asio::ip::tcp::socket socket;
  const std::string address;
  const std::string port;
};

#endif //CONNECTION_H_