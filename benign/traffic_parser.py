import argparse
import pathlib
from scapy.all import *
from scapy.layers.inet import TCP, UDP, IP
from scapy.layers.tls.record import TLS
import pandas as pd

def duration(packets):
    # timestamp 값을 이용해서 이전 패킷과의 시간 간격을 계산하고 이를 duration으로 사용
    duration_list = []
    time_list = []

    for i in range(len(packets)):
        duration_list.append(packets[i].time)
        
    k = duration_list[0]
    time_list = [f"{i - k:.6f}" for i in duration_list]
    
    return time_list

def tx_byte(packets):

    tx_bytes = []

    for packet in packets:
        if IP in packet:
            if "192.168" in packet[IP].src:
                tx_byte = len(packet)
            else:
                tx_byte = -len(packet)
        tx_bytes.append(tx_byte)

    return tx_bytes

if __name__ == '__main__':
    files = [f for f in pathlib.Path().glob("facebook.com/*")]
    for filename in files:
        packets = rdpcap(str(filename))

        duration_value = duration(packets)
        tx_byte_value = tx_byte(packets)

        data = {
            "DURATION": duration_value,
            "TX Bytes": tx_byte_value,
        }
        df = pd.DataFrame(data)
        name = str(filename).replace('.pcap','')
        name = name.replace('facebook.com/','')
        df.to_csv("parse/%s.csv"%(name), index=None)
    