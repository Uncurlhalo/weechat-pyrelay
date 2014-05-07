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
myRelay.close()