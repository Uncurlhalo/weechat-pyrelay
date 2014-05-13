#!/usr/bin/env python3
import datetime
import relay
import color
import time
import os

class WeechatBuffer():
	def __init__(self, path, full_name, short_name, title, relay=None):
		self.lines = []
		self.nicklist = WeechatNickList()
		self.path = path
		self.full_name = full_name
		self.short_name = short_name
		self.title = title
		self.relay = relay
		self.prefixWidth = None
		self.nickWidth = None
		self.MAX_NICK_WIDTH = 0

	def updateLines(self):
		lines = []
		if self.relay:
			self.relay.send("(listlines) hdata buffer:{0}/own_lines/last_line(-200)/data date,displayed,prefix,message".format(self.path))
		else:
			return False
		reply = self.relay.recieve()
		linesItems = reply.objects[0].value['items']
		for item in linesItems:
			displayed = bool(item['displayed'])
			message = item['message']
			prefix = item['prefix']
			date = item['date']
			lines.append(WeechatLine(message, date, prefix, displayed))
		lines.reverse()
		self.lines = lines
		return True

	def addLine(self, message, prefix="   "):
		self.lines.append(WeechatLine(message, int(time.time()), prefix, True))

	def updateNicks(self):
		nicklist = WeechatNickList()
		if self.relay:
			self.relay.send('(nicklist) nicklist {0}'.format(self.path))
		else:
			return False
		reply = self.relay.recieve()
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
		return True

	def getPrefixWidth(self):
		longest = 0
		for line in self.lines:
			prefix = color.remove(line.prefix)
			length = len(prefix)
			if length > longest:
				longest = length
		self.prefixWidth = longest

	def getNickWidth(self):
		longest = 0
		# if the max nick width has been set then use that as nickWidth, otherwise find the longest prefix+nick combo
		if self.MAX_NICK_WIDTH:
			self.nickWidth = self.MAX_NICK_WIDTH
		else:
			for nick in nicklist.nicks:
				nick_val = nick.prefix + nick.name
				length = len(nick_val)
				if length > longest:
					longest = length
			self.nickWidth = longest

	def __str__(self):
		# TODO: The number of lines to be printed to the TTY needs to be 3 lines less than its total height, this allows the title at the top and then a status line plus the input line at the bottom
		# TODO: Get the nick list printed next to the lines of text from buffers, similar to how it is done in the weechat interface.
		ret = ""
		if not self.prefixWidth:
			self.getPrefixWidth()
		#if not self.nickWidth:
		#	self.getNickWidth()
		rows, columns = os.popen('stty size', 'r').read().split()
		for line in self.lines:
			dt = datetime.datetime.fromtimestamp(line.date)
			if self.short_name and len(self.lines): 
				prefix_str = "{0} {1} {2}{3}".format(dt.strftime('%X'), self.short_name.rjust(len(self.short_name)), color.remove(line.prefix).rjust(self.prefixWidth), " | ")
				message_str = color.remove(line.message)
				# adjust for tty width
				ret += prefix_str + message_str[:(int(columns) - len(prefix_str))]
				message_str = message_str[(int(columns) - len(prefix_str)):]
				while len(message_str) > 0:
					ret += ' '*(len(prefix_str)-2) + '| '
					ret += message_str[:(int(columns) - len(prefix_str))]
					message_str = message_str[(int(columns) - len(prefix_str)):] 
				ret += '\n'
			elif line.prefix and len(self.lines):
				prefix_str = "{0} {1}{2}".format(dt1.strftime('%X'), color.remove(line.prefix).rjust(self.prefixWidth), " | ")
				message_str = color.remove(line.message)
				# adjust for tty width
				ret += prefix_str + message_str[:(int(columns) - len(prefix_str))]
				message_str = message_str[(int(columns) - len(prefix_str)):]
				while len(message_str) > 0:
					ret += ' '*(len(prefix_str)-2) + '| '
					ret += message_str[:(int(columns) - len(prefix_str))]
					message_str = message_str[(int(columns) - len(prefix_str)):]
				ret += '\n'
			elif len(self.lines):
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
