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

updateUI = 1

class Networker(threading.Thread):
    def __init__(self, buffers, lock, has_quit):
        threading.Thread.__init__(self)
        self.has_quit = has_quit
        self.buffers = buffers
        self.lock = lock

    def run(self):
        global updateUI
        # just wait for a reply, once we get it pass it on and try
        # to read again cause sync will be sending lots of messages
        while not self.has_quit:
            reply = myRelay.recieve()
            self.lock.acquire()
            if syncing.processReply(reply, self.buffers):
                updateUI += 1
            self.lock.release()

class UIHandler(threading.Thread):
    def __init__(self, buffers, current_buffer, lock, has_quit):
        threading.Thread.__init__(self)
        self.current_buffer = current_buffer
        self.has_quit = has_quit
        self.buffers = buffers
        self.lock = lock

    def run(self):
        global updateUI
        rows, columns = os.popen('stty size', 'r').read().split()
        columns = int(columns)
        while not self.has_quit:
            if updateUI:
                self.lock.acquire()
                # get title line formated
                if buffers[current_buffer].title:
                    title_str = (buffers[current_buffer].title[:columns]).ljust(columns)
                else:
                    title_str = (" "[:columns]).ljust(columns)
                title_str = '\033[1;44m' + title_str + '\033[0m'
                print(title_str)
                if len(str(buffers[current_buffer])):
                    print(buffers[current_buffer], end="")
                # get status line formated
                if buffers[current_buffer].full_name:
                    status_line = (buffers[current_buffer].full_name[:columns]).ljust(columns)
                else:
                    status_line = (" "[:columns]).ljust(columns)
                status_line = '\033[1;44m' + status_line + '\033[0m'
                print(status_line)
                updateUI -= 1
                self.lock.release()
            
                

has_quit = False

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

# Initialize data structure and create all the buffers that exist in the remote session
buffers = {}
bufferItemList = reply.objects[0].value['items']
for item in bufferItemList:
    full_name = item['full_name']
    short_name = item['short_name']
    path = item['__path'][0]
    title = item['title']
    buffers[full_name] = objs.WeechatBuffer(path, full_name, short_name, title, myRelay)
for key in buffers.keys():
    if not buffers[key].updateLines():
        buffers[key].relay = myRelay
    if not buffers[key].updateNicks():
        buffers[key].relay = myRelay

# Create a menu buffer which should keep track of all the buffers that can be accesed through the client
buffers['client.menu'] = objs.WeechatBuffer('0x0000000', 'client.menu', 'menu', 'weechat-pyrelay buffer menu', myRelay)
# we need to build the lines in the buffer
buffers['client.menu'].addLine("Available buffers:", "=!=")
for key in buffers.keys():
    buffers['client.menu'].addLine("   > " + key)
buffers['client.menu'].addLine("To open a buffer type /open followed by the buffer name as shown above next to each >.")

current_buffer = 'client.menu'

myRelay.send('sync')

lock = threading.Lock()
network_Thread = Networker(buffers, lock, has_quit)
ui_Thread = UIHandler(buffers, current_buffer, lock, has_quit)
network_Thread.start()
ui_Thread.start()

while not has_quit:
    while updateUI:
        pass
    message = input("input> ")
    if '/close' in message.split():
        if current_buffer == 'client.menu':
            has_quit = True
        else:
            current_buffer = 'client.menu'
            updateUI += 1
    elif '/quit' in message.split():
        has_quit = True
    elif '/help' in message.split():
        buffers['client.menu'].addLine("[Help Message]")
        buffers['client.menu'].addLine(" Type /open and a buffer number to open that remote buffer and begin sending messages to it")
        buffers['client.menu'].addLine(" Type /locbuffers to get a list of the buffers available to the client")
        buffers['client.menu'].addLine(" Type /quit to exit the program (Note: currently broken, only exits main thread. Must ctrl^c to fully exit)")
        if current_buffer == 'client.menu':
            updateUI += 1
    elif '/locbuffers' in message.split():
        buffers['client.menu'].addLine("Available buffers:", "=!=")
        for key in buffers.keys():
            buffers['client.menu'].addLine("   > " + key)
        if current_buffer == 'client.menu':
            updateUI += 1
    elif '/open' in message.split():
        new_buf = message.split()[1]
        if new_buf in buffers.keys():
            current_buffer = new_buf
            updateUI += 1
        else:
            buffers['client.menu'].addLine("Invalid buffer, please enter a valid buffer name")
            updateUI += 1
    elif '/debug' in message.split():
        print("current buffer = " + current_buffer)
    else:
        if current_buffer == 'client.menu':
            pass
        elif message:
            myRelay.send('input {0} {1}'.format(buffers[current_buffer].path, message))
            updateUI += 1

# TODO: fix the closing of all child threads when the has_quit condition goes True. This should be functional as the has_quit condition determines whether or not the children keep looping looking for updates
network_Thread.join()
ui_Thread.join()