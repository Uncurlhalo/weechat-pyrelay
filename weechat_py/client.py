import relay
import yaml
import argparse

parser = argparse.ArgumentParser(description='Parse some args yo')
parser.add_argument('--password', '-p', type=str)
args = parser.parse_args()

config = yaml.load(open('conf.yaml', 'r'))
host = config['Host']
port = config['Port']
IPv6 = config['IPv6']
ssl = config['SSL']

myRelay = relay.WeechatRelay(host, port, IPv6, ssl)
myRelay.init(args.password)

myRelay.send('(listbuffers) hdata buffer:gui_buffers(*) number,full_name,short_name,type,nicklist,title,local_variables')
buffer_list = myRelay.recieve()
myRelay.send('(listlines) hdata buffer:gui_buffers(*)/own_lines/last_line(-50)/data date,displayed,prefix,message')
lines = myRelay.recieve()
myRelay.send('(nicklist) nicklist')
nicklist = myRelay.recieve()
myRelay.send('sync')

