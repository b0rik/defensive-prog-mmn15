#include <boost/asio.hpp>
#include <iostream>
#include <iomanip>
#include "settings.h"
#include "connection.h"

#include "payload.h"
#include "header.h"
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


const INFO_FILE = "transfer.info";
const USER_FILE = "me.info";
const KEY_FILE = "priv.key";
int main () {
  Settings settings("transfer.info", "me.info");
  RequestProvider request_provider(settings);
  SerializerBytes serializer;
  ResponseHandler response_handler(settings);

  Connection connection(settings.get_address(), settings.get_port());
  connection.connect();

  if (settings.user_exists()) {
    request = request_provider.get_request(OPS.login);
  } else {
    request = request_provider.get_request(OPS.register);
  }

  serialized_request = request.serialize(serializer);
  connection.write(serialized_request);

  while (true) {
    serialized_response = connection.read();
    response = serialized.deserialize(resialized_response);

    if (response.get_header().get_code() == OP.end) {
      break;
    }

    response_handler.handle(response);
  }
}