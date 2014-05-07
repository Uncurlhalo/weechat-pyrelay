WeeChatConnection: include/WeeChatConnection.h src/WeeChatConnection.cpp
	clang++ -Wall -pedantic -shared -Wl,-soname,WeeChatConnection -o WeeChatConnection.so -fPIC src/WeeChatConnection.cpp

clean:
	rm WeeChatConnection.so
