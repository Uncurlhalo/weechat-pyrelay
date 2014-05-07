#!/usr/bin/env python3
import yaml
import color
import relay
import datetime
import weechatObjects as objs

config = yaml.load(open('conf.yaml', 'r'))
host = config['Host']
port = config['Port']
IPv6 = config['IPv6']
ssl = config['SSL']
mypassword = config['Password']
myRelay = relay.WeechatRelay(host, port, IPv6, ssl)
myRelay.init(mypassword)

def bufferInit():
	ret = {}
	myRelay.send('(listbuffers) hdata buffer:gui_buffers(*) number,full_name,short_name,type,nicklist,title,local_variables')
	reply = myRelay.recieve()
	bufferItemList = reply.objects[0].value['items']

	# now we populate the buffers dict from the list of items
	for item in bufferItemList:
		full_name = item['full_name']
		short_name = item['short_name']
		path = item['__path'][0]
		title = item['title']
		ret[full_name] = objs.WeechatBuffer(path, full_name, short_name, title)

	# For each buffer object update its lines and update the nicks in buffer
	for key in ret.keys():
		ret[key].updateLines(myRelay)
		ret[key].updateNicks(myRelay)

	return ret

buffers = bufferInit()
# This section deals only with handling the data requested in the sections above
# Right now it only prints the data in a resonably clean format
for key,buf in buffers.items():
	print("Buffer {0} content:".format(key))
	print(buf)
	print("Buffer {0} nicklist:".format(key))
	print(buf.nicklist)

# TODO: the sync command will cause the remote relay to push any changes to clients.
# This will be very helpful since it means polling the remote session isnt necessary, instead we can just wait for messages to arrive on the socket.
# There will be the issue of when nothing has changed in the remote session, the socket will be locked waiting for data which will cause blocking.
# Therefore a method of having the socket listening and updating the local data structures needs to exist, while a second process will be waiting for user input
# and sending their new messages to the buffer they are viewing. This process will also handle escape sequences to change to different buffers as well as the 
# drawing of the interface. This could be possible through threads or something like it, or state machine style coding.

myRelay.close()