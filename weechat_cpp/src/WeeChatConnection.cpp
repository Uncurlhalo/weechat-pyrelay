#include "../include/WeeChatConnection.h"

#include <string>
#include <iostream>
#include <errno.h>
#include <cstdio>
#include <cstdlib>

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
    if (send(this->sockfd, init_string.c_str(), init_string.size(), 0) == -1)
    {
        throw CommunicationException("Could not send init message!");
    } 
}

void WeeChatConnection::send_msg(std::string message)
{
    std::string message_string = message + "\n";
    if (send(this->sockfd, message_string.c_str(), message_string.size(), 0) == -1)
    {
        throw CommunicationException(std::string("Could not send message ") + message);
    }   
}

std::string WeeChatConnection::receive()
{
    char *message_str = new char[4];

    int n = recv(this->sockfd, message_str, 4, 0);
    if (n < 0)
        throw CommunicationException(std::string("Failed to receive data"));
    
    size_t size = ntohl(*(uint32_t*)message_str); 
    
    if ( ( message_str = (char*)realloc(message_str, size)) == NULL)
        throw WeeChatAllocationException(std::string("Could not allocate space for message"));

    n = recv(this->sockfd, message_str+4, size-4, 0);
     
    std::string return_string(message_str, size);    
  
    delete[] message_str;
    
    return return_string;
}

void WeeChatConnection::close()
{
    if (shutdown(this->sockfd, 2))
        throw CommunicationException(std::string("Could not close socket!"));

}
