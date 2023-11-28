#ifndef CLIENT_H_
#define CLIENT_H_

#include <boost/asio.hpp>
#include <string>

class Client {
public:
  Client(boost::asio::io_context& io_context, const std::string& address, const std::string& port);
  void connect(); // add error handling maybe error return value
  void send();
  void receive();
private:
  boost::asio::io_context& io_context;
  boost::asio::ip::tcp::socket socket;
  const std::string address;
  const std::string port;
};

#endif //CLIENT_H_