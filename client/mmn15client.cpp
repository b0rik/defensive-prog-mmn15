#include <boost/asio.hpp>
#include "settings.h"
#include "client.h"

int main() {
  Settings settings("transfer.info", "me.info");
  
  boost::asio::io_context io_context;
  Client client(io_context, settings.get_address(), settings.get_port());
  client.connect(); // add error handling

  if (settings.user_exists()) { 
    // relogin
  } else {
    // register

  return 0;
}