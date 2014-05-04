import ctypes

class WeeChatConnection:
    def __init__(self):
        self.library = ctypes.CDLL('./WeeChatConnection.so')
        self.class_ptr = self.library.WeeChatConnection_constr()
    
    def init(self, server, port, ipv6, ssl):
        self.library.WeeChatConnection_init(self.class_ptr, server, port, ipv6, ssl)
    
    def SendMessage(self, message):
        str_p = ctypes.c_char_p(self.library.WeeChatConnection_send_msg(self.class_ptr, message))
        str = str_p.value
        self.library.free_buf(str_p)
        return str
    
    def __del__(self):
        self.library.WeeChatConnection_destroy(self.class_ptr)

if __name__ == '__main__':
    wcc = WeeChatConnection()
    wcc.init("www.google.com", 21, False, True)
    print(wcc.SendMessage("Message!"))
