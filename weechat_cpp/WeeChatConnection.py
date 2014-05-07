import ctypes

class WeeChatConnection:
    def __init__(self, server, port, ipv6, ssl):
        self.library = ctypes.CDLL('./WeeChatConnection.so')
        self.class_ptr = self.library.WeeChatConnection_constr(server, port, ipv6, ssl)
    
    def init(self, password):
        self.library.WeeChatConnection_init(self.class_ptr, password)
    
    def SendMessage(self, message):
        self.library.WeeChatConnection_send_msg(self.class_ptr, message)
    
    def __del__(self):
        self.library.WeeChatConnection_destroy(self.class_ptr)

if __name__ == '__main__':
    wcc = WeeChatConnection('128.173.88.125', 9000, False, False)
    wcc.init("rytuoiyt")
    wcc.SendMessage("info version")
