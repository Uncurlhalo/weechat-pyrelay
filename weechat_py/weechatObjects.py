#!/usr/bin/env python3
import relay
import color
import os

class WeechatBuffer():
	def __init__(self, path, full_name, short_name, title):
		self.lines = []
		self.nicklist = WeechatNickList()
		self.path = path
		self.full_name = full_name
		self.short_name = short_name
		self.title = title
		self.prefixWidth = None
		self.nickWidth = None

	def updateLines(self, therelay):
		lines = []
		therelay.send("(listlines) hdata buffer:{0}/own_lines/last_line(-200)/data date,displayed,prefix,message".format(self.path))
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
		rows, columns = os.popen('stty size', 'r').read().split()
		for line in reversed(self.lines):
			if self.short_name: 
				prefix_str = "{0} {1}{2}".format(self.short_name.rjust(len(self.short_name)), color.remove(line.prefix).rjust(self.prefixWidth), " | ")
				message_str = color.remove(line.message)
				ret += prefix_str + message_str[:(int(columns) - len(prefix_str))]
				message_str = message_str[(int(columns) - len(prefix_str)):]
				while len(message_str) > 0:
					ret += ' '*(len(prefix_str)-2) + '| '
					ret += message_str[:(int(columns) - len(prefix_str))]
					message_str = message_str[(int(columns) - len(prefix_str)):] 
				ret += '\n'
			elif line.prefix:
				prefix_str = "{0}{1}".format(color.remove(line.prefix).rjust(self.prefixWidth), " | ")
				message_str = color.remove(line.message)
				ret += prefix_str + message_str[:(int(columns) - len(prefix_str))]
				message_str = message_str[(int(columns) - len(prefix_str)):]
				while len(message_str) > 0:
					ret += ' '*(len(prefix_str)-2) + '| '
					ret += message_str[:(int(columns) - len(prefix_str))]
					message_str = message_str[(int(columns) - len(prefix_str)):]
				ret += '\n'
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
	def __init__(self, name, prefix, color, visible):
		self.name = name
		self.prefix = prefix
		self.color = color
		self.visible = visible

class WeechatNickList():
	def __init__(self):
		self.nicks = []
		self.nickWidth = None

	def addNick(self, newNick):
		self.nicks.append(newNick)

	def getNickWidth(self):
		longest = 0
		for nick in rself.nicks
			length = len(nick.prefix + nick.name)
			if length > longest:
				longest = length
		return longest

	def __str__(self):
		ret = ""
		if not self.nickWidth:
			self.nickWidth = self.getNickWidth()
		for nick in self.nicks:
			if nick.visible:
				temp = "{0}{1}".format(nick.prefix, nick.name)
				if len(temp) > nickWidth:
					ret = ret + temp[:(nickWidth - 1)] + "+\n"
				else:
					ret = ret + temp + "\n"
			else:
				ret = ret
		return ret
