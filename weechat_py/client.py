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

updateUI = 0

class Networker(threading.Thread):
    def __init__(self, buffers, lock):
        threading.Thread.__init__(self)
        self.buffers = buffers
        self.lock = lock

    def run(self):
        global updateUI
        # just wait for a reply, once we get it pass it on and try
        # to read again cause sync will be sending lots of messages
        while True:
            reply = myRelay.recieve()
            self.lock.acquire()
            if syncing.processReply(reply, self.buffers):
                updateUI += 1
            self.lock.release()

class UIHandler(threading.Thread):
    def __init__(self, buffers, lock):
        threading.Thread.__init__(self)
        self.buffers = buffers
        self.lock = lock

    def run(self):
        global updateUI
        while True:
            self.lock.acquire()
            if updateUI:
                # TODO: Figure out UI things
                # we update UI shit, meaning that the sync message pertains to the currently viewed buffer or the whole client interface
                print("UI had to update")
                updateUI -= 1
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

lock = threading.Lock()
network_Thread = Networker(buffers, lock)
ui_Thread = UIHandler(buffers, lock)
network_Thread.start()
ui_Thread.start()

myRelay.send('input core.weechat /help')
myRelay.send('input core.weechat /reconnect oftc')

while True:
    # TODO: decide how to do grabbing of input on last row
    # here we should loop forever in the main thread capturing user input and sending it as "input" messages to the relay
    print("grabbed input")