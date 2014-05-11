#!/usr/bin/env python3
import os
import sys
import yaml
import color
import relay
import datetime
import threading
import weechatSync as syncing
import weechatObjects as objs

class Networker(threading.Thread):
    def __init__(self, buffers, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.buffers = buffers

    def run():
        # just wait for a reply, once we get it pass it on and try
        # to read again cause sync will be sending lots of messages
        while True:
            reply = myRelay.recieve()
            self.lock.acquire()
            syncing.processReply(reply, self.buffers)
            self.lock.release()

config = yaml.load(open('conf.yaml', 'r'))
mypassword = config['Password']
host = config['Host']
port = config['Port']
IPv6 = config['IPv6']
ssl = config['SSL']
# Initialize
myRelay = relay.WeechatRelay(host, port, IPv6, ssl)
myRelay.init(mypassword)
# Send first data
myRelay.send('(listbuffers) hdata buffer:gui_buffers(*) number,full_name,short_name,type,nicklist,title,local_variables')
reply = myRelay.recieve()
bufferItemList = reply.objects[0].value['items']
# Initialize data structure
buffers = {}
for item in bufferItemList:
    full_name = item['full_name']
    short_name = item['short_name']
    path = item['__path'][0]
    title = item['title']
    buffers[full_name] = objs.WeechatBuffer(path, full_name, short_name, title)
for key in buffers.keys():
    buffers[key].updateLines(myRelay)
    buffers[key].updateNicks(myRelay)

myRelay.send('sync')
myRelay.send('input core.weechat \help')

lock = threading.Lock()
network_Thread = Networker(buffers, lock)
network_Thread.start()

print(buffers['core.weechat'])

class Networker(threading.Thread):
    def __init__(self, buffers, lock):
        super(Networker, self).__init__()
        self.lock = lock
        self.buffers = buffers

    def run(self):
        # just wait for a reply, once we get it pass it on and try
        # to read again cause sync will be sending lots of messages
        while True:
            reply = myRelay.recieve()
            self.lock.acquire()
            syncing.processReply(reply, self.buffers)
            self.lock.release()