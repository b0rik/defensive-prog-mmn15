#include <vector>
#include "settings.h"
#include "message.h"
#include "request_header.h"
#include "response_header.h"
#include "request_payload.h"

int main() {
  Settings settings("transfer.info", "me.info");

  if (settings.id_exists()) { // need to be if me.info exists
    // relogin
  } else {
    // register
    // create request
    Payload *payload = new RequestUserPayload(settings.get_name());
    Header *header = new RequestHeader(settings.get_id(), VERSION, 1025, payload->get_size());
    Message request = Message(*header, *payload);
    
    // pack request
    std::vector<uint8_t> request_bytes = request.serialize();
  } 

  /*
    --Register--
      send 1025
      -make payload
      -make header
      -make message
      -serialize message
        little endian byte stream of members
      -send message
        create connection 
        send bytes
        receive 2100 client id
          send 1026 public key
            receive 2102 aes key
              send 1028 file
                receive 2103 crc
                  send 1029 crc ok
                    receive 2104 ok
                      terminate
                    or
                    receive 2107 error
                  or
                  send 1030 crc fail
                    send 1028 file
                      repeat
                  or
                  send 1031 crc fail x3
                    terminate
                or
                receive 2107 error
            or
            receive 2107 error
        or
        receive 2101 fail
  */

  return 0;
}