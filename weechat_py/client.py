import yaml
import color
import relay
import datetime
import argparse
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

# For each buffer object get its last 100 lines
# Make the buffers.lines value equal to the new list of lines
for key,value in buffers.items():
	lines = []
	times = []
	myRelay.send("(listlines) hdata buffer:{0}/own_lines/last_line(-100)/data date,displayed,prefix,message".format(value.path))
	reply = myRelay.recieve()
	linesObject = reply.objects[0]
	linesItems = linesObject.value['items']
	for item in linesItems:
		times.append(item['date'])
		lines.append(item['message'])
	lines.reverse()
	times.reverse()
	buffers[key].lines = lines
	buffers[key].times = times
	buffers[key].items = linesItems

# This section deals only with handling the data requested in the sections above
# Right now it only prints the data in a resonably clean format
for key,buf in buffers.items():
	index = 0
	print("Buffer {0} content:".format(key))
	for line in buf.lines:
		if buf.times[index] != 0:
			ts = datetime.datetime.fromtimestamp(buf.times[index]).strftime('%H:%M:%S')
		else:
			ts = None
		index += 1
		output = color.remove(line)
		if ts:
			print(ts + " | " + output)
		else:
			print(output)
	print("\n")

myRelay.send('(nicklist) nicklist')
nicklist = myRelay.recieve()
nicklist =  nicklist.objects[0]
myRelay.send('sync')

