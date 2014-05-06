import yaml
import relay
import argparse
import weechatObjects as objs

parser = argparse.ArgumentParser(description='Parse some args yo')
parser.add_argument('--password', '-p', type=str)
args = parser.parse_args()

config = yaml.load(open('conf.yaml', 'r'))
host = config['Host']
port = config['Port']
IPv6 = config['IPv6']
ssl = config['SSL']

myRelay = relay.WeechatRelay(host, port, IPv6, ssl)
myRelay.init(args.password)

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
for key,path in buffers.items():
	lines = []
	myRelay.send("(listlines) hdata buffer:{0}"
				  "/own_lines/last_line(-50)/data "
				  "date,displayed,prefix,message".format(path))
	reply = myRelay.recieve()
	linesObject = reply.objects[0]
	linesItemList = linesObject.value['items']
	for item in linesItemList:
		lines.append(item['message'])

	buffers[key].lines = lines

myRelay.send('(nicklist) nicklist')
nicklist = myRelay.recieve()
nicklist =  nicklist.objects[0]
myRelay.send('sync')

