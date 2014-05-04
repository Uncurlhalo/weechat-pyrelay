#ifndef WEECHAT_CONNECTION_H
#define WEECHAT_CONNECTION_H

#include <string>
#include <cstring>

class WeeChatConnection
{
public:
    WeeChatConnection();
    void init(std::string server, int port, bool ipv6, bool ssl);
    std::string send_msg(std::string message);
};

//python wrappings
extern "C"
{
    WeeChatConnection *WeeChatConnection_constr()
    {
        return new WeeChatConnection();
    }

    void WeeChatConnection_init(WeeChatConnection* self,
                                char* server,
                                int port,
                                bool ipv6,
                                bool ssl)
    {
        self->init(server, port, ipv6, ssl);
    }

    char *WeeChatConnection_send_msg(WeeChatConnection* self, char *message)
    {
        std::string ret = self->send_msg(message);
        char* array = new char[ret.size()+1];
        strcpy(array, ret.c_str());
        return array;
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
