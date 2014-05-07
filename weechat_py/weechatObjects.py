#!/usr/bin/env python3
import relay
import color

class WeechatBuffer():
	def __init__(self, path, full_name, short_name, title):
		self.lines = []
		self.nicklist = WeechatNickList()
		self.path = path
		self.full_name = full_name
		self.short_name = short_name
		self.title = title
		self.prefixWidth = None

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
		nicklist = WeechatNickList()
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
				nicklist.addNick(WeechatNick(name, prefix, color, visible))
		self.nicklist = nicklist

	def getPrefixWidth(self):
		longest = 0
		for line in reversed(self.lines):
			prefix = color.remove(line.prefix)
			length = len(prefix)
			if length > longest:
				longest = length
		self.prefixWidth = longest

	def __str__(self):
		ret = ""
		if not self.prefixWidth:
			self.getPrefixWidth()
		for line in reversed(self.lines):
			if self.short_name:
				### FIXME: Currently color stripping is hard coded, this should be configurable
				ret += "{0} {1}{2}{3}\n".format(self.short_name.rjust(len(self.short_name)), color.remove(line.prefix).rjust(self.prefixWidth), " | ", color.remove(line.message))
			elif line.prefix:
				### FIXME: Currently color stripping is hard coded, this should be configurable
				ret += "{0}{1}{2}\n".format(color.remove(line.prefix).rjust(3), " | ", color.remove(line.message))
			else:
				### FIXME: Currently color stripping is hard coded, this should be configurable
				ret += "{0}\n".format(color.remove(line.message))
		return ret

class WeechatLine():
	def __init__(self, message, date, prefix, displayed):
		self.displayed = displayed
		self.message = message
		self.prefix = prefix
		self.date = date

class WeechatNick():
	def __init__(self, name, prefix, color, visible):
		self.name = name
		self.prefix = prefix
		self.color = color
		self.visible = visible

class WeechatNickList():
	def __init__(self):
		self.nicks = []

	def addNick(self, newNick):
		self.nicks.append(newNick)

	def __str__(self):
		ret = ""
		for nick in self.nicks:
			if nick.visible:
				ret += "{0}{1}\n".format(nick.prefix, nick.name)
			else:
				ret = ret
		return ret
	