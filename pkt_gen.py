from scapy.all import *
import argparse

data_size = 1400

dst_ip = '10.10.10.1'
dst_port = 55555

src_ip = '10.10.10.2'
src_port = 55556

parser = argparse.ArgumentParser()
parser.add_argument('--dst-ip', dest='dst_ip', default=dst_ip, type=str)
parser.add_argument('--dst-port', dest='dst_port', default=dst_port, type=int)
parser.add_argument('--data-size', dest='data_size', default=data_size, type=int)
args = parser.parse_args()

data = '0' * args.data_size

send(IP(dst=args.dst_ip, src=src_ip)/UDP(dport=args.dst_port, sport=src_port)/Raw(load=data))

