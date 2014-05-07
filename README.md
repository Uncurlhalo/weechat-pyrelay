weechat-pyrelay
===============

### Objective
- Create a simple a simple library for communicating with remote Weechat sessions using the Weechat-relay plugin and protocol.
- Create a simple reference client which demonstrates a method of using the library to create a simple CLI client using the Uwrid pyhton library.
- Support SSL and IPv6

### Purpose
This project is meant to fulfil final assingment in the ECE 2524 - Intro to Unix course at Virginia Tech

### Prototype
This project requires you to have properly configured the weechat-relay plugin on your weechat process. Setting this up is beyond the scope of this project. Instructions to do so can be found here: http://meskarune.tumblr.com/post/43313352409/relay-weechat-irc-messages

The latest usable prototype will be available in the weechat_py/ directory. Run the following to test the prototype.

    git clone https://github.com/Uncurlhalo/weechat-pyrelay
    cd weechat-pyrelay/weechat_py/

Edit `conf.yaml` in the editor of your choice. You must change the Host, Port, and Password fields to match your weechat-relays settings. After the conf.yaml file contains the correct settings execute the following to run the actual prototype.

    chmod +x ./client.py
    ./client.py

The information returned is information about your remote weechat-relay session. It includes get a list of all buffers, their last 200 lines, and a list of nicks for each buffer.

### Additional Notes

The weechat-pyrelay project utilizes some source from QWeechat available at https://github.com/weechat/qweechat.
