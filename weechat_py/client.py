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
