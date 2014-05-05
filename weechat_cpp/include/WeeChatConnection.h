#ifndef WEECHAT_CONNECTION_H
#define WEECHAT_CONNECTION_H

#include <string>
#include <cstring>
#include <exception>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>


class SocketException : public std::exception
{
private:
    std::string what_string;
public:
    SocketException(std::string what_string)
    {
        this->what_string = what_string;
    }
    
    virtual const char* what() const throw()
    {
        return what_string.c_str();
    }
    ~SocketException() throw() {}
};

class CommunicationException : public std::exception
{
private:
    std::string what_string;
public:
    CommunicationException(std::string what_string)
    {
        this->what_string = what_string;
    }
    virtual const char* what() const throw()
    {
        return what_string.c_str();
    }
    ~CommunicationException() throw() {}
};

class WeeChatConnection
{
private:
    int sockfd;
    sockaddr_in serv_addr;
    hostent *server;
    
public:
    WeeChatConnection(std::string server, int port, bool ipv5, bool ssl);

    void init(std::string password);
    void send_msg(std::string message);
};

//python wrappings
extern "C"
{
    void WeeChatConnection_init(WeeChatConnection *self, char* password)
    {
        self->init(password);
    }

    WeeChatConnection *WeeChatConnection_constr(char* server,
                                                int port,
                                                bool ipv6,
                                                bool ssl)
    {
        return new WeeChatConnection(server, port, ipv6, ssl);
    }

    void WeeChatConnection_send_msg(WeeChatConnection* self, char *message)
    {
        self->send_msg(message);
    }

    void free_buf(char* buf)
    {
        delete[] buf;
    }

    void WeeChatConnection_destroy(WeeChatConnection* self)
    {
        delete self;
    }

}

#endif
