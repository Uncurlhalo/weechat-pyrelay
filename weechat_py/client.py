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

# First get a list of buffers and create a buffer object for each
myRelay.send('(listbuffers) hdata buffer:gui_buffers(*) number,full_name,short_name,type,nicklist,title,local_variables')
reply = myRelay.recieve()
buffers = {}
bufferObject = reply.objects[0]
bufferItemList = bufferObject.value['items']
for item in bufferItemList:
	name = item['full_name']
	path = item['__path'][0]
	buffers[name] = objs.WeechatBuffer(path, name)

# For each buffer object update its lines and update the nicks in buffer
for key,value in buffers.items():
	buffers[key].updateLines(myRelay)
	buffers[key].updateNicks(myRelay)

# This section deals only with handling the data requested in the sections above
# Right now it only prints the data in a resonably clean format
for key,buf in buffers.items():
	index = len(buf.times) - 1
	print("Buffer {0} content:".format(key))
	for line in reversed(buf.lines):
		if buf.times[index] != 0:
			ts = datetime.datetime.fromtimestamp(buf.times[index]).strftime('%H:%M:%S')
		else:
			ts = None
		index -= 1
		output = color.remove(line)
		if ts:
			print(ts + " | " + output)
		else:
			print(output)
	print("\n")

for key,buf in buffers.items():
	print("{0} nickslist:".format(key))
	print(buf.nicks)
	print("\n")

myRelay.send('sync')