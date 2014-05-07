weechat-bouncer
===============

The project objective is to create a simple library for communicating with a running instance of weechat using the weechat-relay protocol.

Additionally a reference client will be built demonstrating how to create and utilize the objects presented by the library. It will also provide a simple interface with weechat allowing a remote user to send and recieve messages from their running weechat session. It will provide both SSL and IPv6 support.

This project is for the final assingment in the VT course ECE 2524 - Intro to Unix

weechat-pyrelay utilizes some source from QWeechat available at https://github.com/weechat/qweechat.

# Prototype
The current functioning prototype is the client.py program in the weechat_py directory.

To run it cd to that directory after cloning the repo and edit the config to provide it the credentials for you weechat-relay

Then run "python3 client.py"

This should print out a section of the last 100 lines in each buffer of your weechat session as well as timestamps for when lines were printed when applicable.

Since this project aims at providing a library for interfacing with relays a large portion of the substance is hidden from view. To appreciate the work done so far I would recommend playing with the various objects provided by the relay.py, protocol.py, and weechatObjects.py files.

As it is still a work in progress there may be bugs as testing and development are still occuring.
