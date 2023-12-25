#include <boost/asio.hpp>
#include <iostream>
#include "session.h"
#include "connection.h"
#include "request_provider.h"
#include "response_handler.h"
#include "message.h"

int main() {
    // init session data
    try {
        std::cout << "initialiing session..." << std::endl;
        Session session;
        std::cout << "session initialized." << std::endl << std::endl;;

        // init connection
        std::cout << "connecting to the server..." << std::endl;
        boost::asio::io_context io_context;
        Connection connection(io_context, session.get_address(), session.get_port());
  
        // connect to server
        //connection.connect();
        //std::cout << "connected to the server." << std::endl << std::endl;

        // set first request
        session.set_request_code(session.get_user_exists() ? 1027 : 1025);

        RequestProvider request_provider(session);
        ResponseHandler response_handler(session);

        // start communication loop
        while (!session.get_is_done()) {
            // generate request
            std::cout << "making request " << session.get_request_code() << std::endl;
            Message request;

            try {
                request_provider.make_request(request);
            } 
            catch (std::exception& e) {
                std::cout << e.what() << std::endl;
                throw std::exception("failed to make request.");
            }
            std::cout << "made request." << std::endl << std::endl;

            // send request
            std::cout << "sending request..." << std::endl;
            connection.connect();
            connection.send(request);
            std::cout << "request sent." << std::endl << std::endl;

            // if current request is 1030 then skip the reading and immediately send request 1028
            if (session.get_request_code() == 1030) {
                session.set_request_code(1028);
                continue;
            }

            // read response
            Message response;
    
            std::cout << "receiving response..." << std::endl;
            connection.receive(response);
            connection.disconnect();
            std::cout << "response received " << response.header.code << std::endl << std::endl;

            // handler response
            std::cout << "handling response..." << std::endl;
            response_handler.handle(response);
            std::cout << "response handled." << std::endl << std::endl;
        }
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
    }
   
    std::cout << "Terminating...\n";
    system("pause");

    return 0; 

}