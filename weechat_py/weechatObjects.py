#!/usr/bin/env python3
import relay
import color

class WeechatBuffer():
	def __init__(self, path, full_name, short_name, title):
		self.lines = []
		self.nicks = []
		self.path = path
		self.full_name = full_name
		self.short_name = short_name
		self.title = title

	def updateLines(self, therelay):
		lines = []
		therelay.send("(listlines) hdata buffer:{0}/own_lines/last_line(-500)/data date,displayed,prefix,message".format(self.path))
		reply = therelay.recieve()
		linesItems = reply.objects[0].value['items']
		for item in linesItems:
			displayed = bool(item['displayed'])
			message = item['message']
			prefix = item['prefix']
			date = item['date']
			lines.append(WeechatLine(message, date, prefix, displayed))
		self.lines = lines

	def updateNicks(self, therelay):
		nicks = []
		therelay.send('(nicklist) nicklist {0}'.format(self.path))
		reply = therelay.recieve()
		nicksItems = reply.objects[0].value['items']
		for item in nicksItems:
			if item['group']:
				pass
			else:
				name = item['name']
				prefix = item['prefix']
				color = item['color']
				visible = bool(item['visible'])
				nicks.append(WeechatNick(name, prefix, color, visible))
		self.nicks = nicks

	def __str__(self):
		ret = ""
		for line in reversed(self.lines):
			if self.short_name:
				ret += "{0} {1}{2}{3}\n".format(self.short_name.rjust(len(self.short_name)), color.remove(line.prefix).rjust(3), " | ", color.remove(line.message))
			elif line.prefix:
				ret += "{0}{1}{2}\n".format(color.remove(line.prefix).rjust(3), " | ", color.remove(line.message))
			else:
				ret += "{0}\n".format(color.remove(line.message))
		return ret

class WeechatLine():
	def __init__(self, message, date, prefix, displayed):
		self.displayed = displayed
		self.message = message
		self.prefix = prefix
		self.date = date

class WeechatNick():
	def __inti__(self, name, prefix, color, visible):
		self.name = name
		self.prefix = prefix
		self.color = color
		self.visible = visible