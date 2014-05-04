#include "../include/WeeChatConnection.h"

#include <string>
#include <iostream>

WeeChatConnection::WeeChatConnection()
{
    std::cout << "Constructor called" << std::endl;
}

void WeeChatConnection::init(std::string server, int port, bool ipv6, bool ssl)
{
    std::cout << "Server " << server << std::endl
              << "port " << port << std::endl
              << "ipv6 " << ipv6 << std::endl
              << "ssl " << ssl << std::endl;
}

std::string WeeChatConnection::send_msg(std::string message)
{
    std::cout << "sending message " << message << std::endl;
    return "lel";
}

