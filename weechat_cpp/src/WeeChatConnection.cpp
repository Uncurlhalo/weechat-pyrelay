#include "../include/WeeChatConnection.h"

#include <string>
#include <iostream>
#include <errno.h>
#include <cstdio>

WeeChatConnection::WeeChatConnection(std::string server,
                                     int port,
                                     bool ipv6,
                                     bool ssl )
{
    this->sockfd = socket( (ipv6 ? AF_INET6 : AF_INET),
                           SOCK_STREAM,
                           IPPROTO_TCP );    

    if (this->sockfd < 0)
        throw SocketException("Could not create socket");

    this->server = gethostbyname(server.c_str());

    if (this->server == NULL)
    {
        throw SocketException("Could not resolve host name");
    }

    bzero((char*) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = (ipv6 ? AF_INET6 : AF_INET);
    std::cout << server << std::endl;
    serv_addr.sin_addr.s_addr = inet_addr(server.c_str());
    serv_addr.sin_port = htons(port);

    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
    {
        perror("qq");
        throw SocketException("Could not connect");
    }
}

void WeeChatConnection::init(std::string password)
{
    std::string init_string = "init password=" + password + "\n";
    if (send(this->sockfd, init_string.c_str(), init_string.size(), 0) != init_string.size())
    {
        throw CommunicationException("Could not send init message!");
    } 
}

void WeeChatConnection::send_msg(std::string message)
{
    std::string message_string = message + "\n";
    if (send(this->sockfd, message_string.c_str(), message_string.size(), 0) != message_string.size())
    {
        throw CommunicationException(std::string("Could not send message ") + message);
    }   
}