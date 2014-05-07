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
import struct
import socket
import protocol

class WeechatRelay:
	def __init__(self, host, port, inet=False, doSSL=False):
		self.host = host
		self.port = port
		if inet:
			self.inet = socket.AF_INET6
		else:
			self.inet = socket.AF_INET
		self.doSSL = doSSL
		self.proto = protocol.Protocol()
		self.sock = socket.socket(self.inet, socket.SOCK_STREAM)

		if doSSL:
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
		buf = b''
		try:
			buf = self.sock.recv(4)
			length = struct.unpack('>i', buf[0:4])[0]
			buf += self.sock.recv(length-4)
		except:
			print("Unable to recieve on the socket, has init been run?")

		message = self.proto.decode(buf)
		return message

	def close(self):
		self.sock.close()