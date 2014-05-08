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

#include <iostream>
#include <algorithm>

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

class WeeChatAllocationException : public std::exception
{
private:
    std::string what_string;
public:
    WeeChatAllocationException(std::string what_string)
    {
        this->what_string = what_string;
    }
    virtual const char* what() const throw()
    {
        return what_string.c_str();
    }
    ~WeeChatAllocationException() throw() {}
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
    std::string receive();
    void close();
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
    
    struct ReceiveData
    {
        size_t arr_size;
        char* arr_ptr;
    };
     
    ReceiveData *WeeChatConnection_receive(WeeChatConnection* self, ReceiveData* rd)
    {
        std::cout << 'a' << std::endl;
        std::string tmp = self->receive();
        std::cout << 'b' << std::endl;
        rd->arr_size = tmp.size();
        rd->arr_ptr = new char[tmp.size()];
        std::cout << 'c' << std::endl;
        memcpy(rd->arr_ptr, tmp.c_str(), tmp.size());
        std::cout << 'd' << std::endl;
        return rd;
    }
    
    void WeeChatConnection_close(WeeChatConnection* self)
    {
        self->close();
    }
}

#endif
