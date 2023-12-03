#include <boost/asio.hpp>
#include <iostream>
#include <iomanip>
#include "settings.h"
#include "connection.h"
// #include "request_provider.h"
// #include "response_handler.h"
#include "message.h"

// int main() {
//   Settings settings("transfer.info", "me.info");
  
//   boost::asio::io_context io_context;
//   Client client(io_context, settings.get_address(), settings.get_port());
//   client.connect(); // add error handling

//   if (settings.user_exists()) { 
//     // relogin
//   } else {
//     // register
//     // create request
//     RequestUserPayload payload(settings.get_name());
//     RequestHeader header("hello", 1, 1025, 255);
//     Message message(header, payload);

//     // serialize request
//     std::vector<uint8_t> request_in_bytes = message.to_bytes();


//     // send request
//     client.write(request_in_bytes);
//     client.read();

//     // for (const auto& byte : response_in_bytes) {
//     //   std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)byte << " ";
//     // }
//   }

//   return 0;
// }


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
  request.header.code = 260;
  request << settings.get_name();
  connection.write(request);
  Message m = connection.read();
  std::cout << m.header.code << std::endl;
  std::cout << m.header.version << std::endl;
  std::cout << m.header.payload_size << std::endl;

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