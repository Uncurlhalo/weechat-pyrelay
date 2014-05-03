#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# relay.py - handle relay objects and their associated connections and objects.
#
# For info about protocol and format of messages, please read document
# "WeeChat Relay Protocol", available at:  http://weechat.org/doc/
#
# History:
#
# 2014-05-03, Jacob Melton:
#     initial development
#
import ssl
import socket
import protocol

class WeechatRelay:
	def __init__(self, host, port, inet=socket.AF_INET, sslenable=False):
		self.host = host
		self.port = port
		self.inet = inet
		self.sslenable = sslenable
		self.proto = protocol.Protocol()
		self.sock = socket.socket(self.inet, socket.SOCK_STREAM)

		if sslenable:
			self.sock = ssl.wrap_socket(self.sock)

	def init(self, password):
		"""
		initialize the relay connection
		actually connect to the socket and use the relay init call
		"""
		self.password = password
		self.sock.connect((self.host, self.port))

		message = "init password={0}\n".format(self.password)
		self.sock.send(message.encode())

	def send(self, message):
		"""
		send a message on the socket
		"""
		message += '\n'
		try:
			self.sock.send(message.encode())
		except:
			print("Unable to send on the socket, has init been run?")

	def recieve(self):
		try:
			buf = self.sock.recv(4096)
		except:
			print("Unable to recieve on the socket, has init been run?")
		if buf:
			message = self.proto.decode(buf)

		return message