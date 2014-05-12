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

	def getNickWidth(self):
		# TODO: implement a way to calculate nick width, this should be over-ridable so the nick column can be forced to be no wider than some max width.
		self.nickWidth = 10

	def __str__(self):
		# TODO: we need to have the number of rows in the string returned by __str__ to be 3 less than height of the tty, so that we can added the title bar and input+status bars
		# TODO: we need to have the width of the returned string equal to the number of colums in the tty minus the width of the nick buffer so that we can print the nick buffer next to the messages
		ret = ""
		if not self.prefixWidth:
			self.getPrefixWidth()
		if not self.nickWidth:
			self.getNickWidth()
		rows, columns = os.popen('stty size', 'r').read().split()
		for line in reversed(self.lines):
			### Note: likely there will need to be something in here to calculate the number of new lines to append if the buffer doesnt naturally fill the row count
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
		for nick in self.nicks:
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
