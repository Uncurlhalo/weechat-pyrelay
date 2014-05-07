#!/usr/bin/env python3
import relay
import color

class WeechatBuffer():
	def __init__(self, path, name):
		self.lines = []
		self.times = []
		self.items = []
		self.nicks = {}
		self.path = path
		self.name = name

	def updateLines(self, therelay):
		lines = []
		times = []
		therelay.send("(listlines) hdata buffer:{0}/own_lines/last_line(-500)/data date,displayed,prefix,message".format(self.path))
		reply = therelay.recieve()
		linesObject = reply.objects[0]
		linesItems = linesObject.value['items']
		for item in linesItems:
			times.append(item['date'])
			lines.append(item['message'])
		self.lines = lines
		self.times = times
		self.items = linesItems

	def updateNicks(self, therelay):
		nicks = {}
		therelay.send('(nicklist) nicklist {0}'.format(self.path))
		reply = therelay.recieve()
		nicksObject = reply.objects[0]
		nicksItems = nicksObject.value['items']
		for item in nicksItems:
			nicks[item['name']] = item['color']
		self.nicks = nicks

	#def __str__(self):
		# since I want to be able to utilize the weechat color codes
		# have a __str__ function is useful since it will allow me to test 
		# parsing the color codes and turning them into logical python
		# for generating color