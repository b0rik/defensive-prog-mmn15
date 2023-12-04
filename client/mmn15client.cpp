#include <boost/asio.hpp>
#include <iostream>
#include <iomanip>
#include "settings.h"
#include "connection.h"
// #include "request_provider.h"
// #include "response_handler.h"
#include "message.h"

const std::string INFO_FILE = "transfer.info";
const std::string USER_FILE = "me.info";
const std::string KEY_FILE = "priv.key";
int main () {
  Settings settings("transfer.info", "me.info");
  // RequestProvider request_provider(settings);
  // ResponseHandler response_handler(settings);

  boost::asio::io_context io_context;
  Connection connection(io_context, settings.get_address(), settings.get_port());
  connection.connect();

  // if (settings.user_exists()) {
  //   request = request_provider.get_request(OPS.login);
  // } else {
  //   request = request_provider.get_request(OPS.register);
  // }
  Message request;
  memcpy(request.header.client_id, "ABCDEFGHIJKLMNOP", 16);
  request.header.version = 1;
  request.header.code = 1025;
  char x[255];
  strncpy(x, settings.get_name().c_str(), 255);
  request << x;
  connection.write(request);
  Message m = connection.read();

  // while (true) {
  //   std::vector<uint8_t> serialized_header;
  //   serialized_header = connection.read(header.header_size);
  //   Header header;
  //   serializer.deserialize(serialized_header, header);

  //   if (header.code == OP.end) {
  //     break;

  //   Payload payload;
  //   std::vector<uint8_t> serialized_payload;
  //   serialized_payload = connection.read(header.payload_size);
  //   }

  //   response_handler.handle(response);
  // }
}