import ctypes
import protocol

class WeeChatConnection:
    def __init__(self, server, port, ipv6, ssl):
        self.library = ctypes.CDLL('./WeeChatConnection.so')
        self.class_ptr = self.library.WeeChatConnection_constr(server, port, ipv6, ssl)
        self.proto = protocol.Protocol()
 
    def init(self, password):
        self.library.WeeChatConnection_init(self.class_ptr, password)
    
    def SendMessage(self, message):
        self.library.WeeChatConnection_send_msg(self.class_ptr, message)
    
    class receiveStruct(ctypes.Structure):
        _fields_=[("size", ctypes.c_int),
                  ("arr", ctypes.POINTER(ctypes.c_char))]

    def receive(self):
        data_str = self.receiveStruct(0, None)        
        print(ctypes.addressof(data_str)) 
        
        self.library.WeeChatConnection_receive(self.class_ptr, ctypes.cast(ctypes.addressof(data_str), ctypes.POINTER(self.receiveStruct)))
                
        print(data_str.size) 
 
        data = []
        for i in range(0, data_str.size):
            data.append(data_str.arr[i])
              
        self.library.free_buf(data_str.arr)
 
        return self.proto.decode(''.join(data))
    
    def close(self):
        self.library.WeeChatConnection_close(self.class_ptr)

    def __del__(self):
        self.library.WeeChatConnection_destroy(self.class_ptr)

if __name__ == '__main__':
    wcc = WeeChatConnection(/*server ip here (sorry, have to fix)*/, 9000, False, False)
    wcc.init(/*password here*/)
    wcc.SendMessage("info version")
    print(wcc.receive())
    wcc.close()
