class weechatRelay
  properties:
    - Host
    - Port
    - IPv4/v6 Flag (optional)
    - SSL/No SSL (optional)
  functions:
    - __init__
	* create socket
	* connect to socket
	* catch network errors 
    - relayInit(password=None)
	* send authentication init message to relay
	* requires password parameter
    - send(message)
    - recieve()
    - decode(message)

class weechatObject
  Use the class provided in the reference example from weechat  
