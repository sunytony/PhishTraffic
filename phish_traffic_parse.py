import argparse
import pathlib
from scapy.all import *
from scapy.layers.inet import TCP, UDP, IP
from scapy.layers.tls.record import TLS
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
import socket


def find_server(packets):
    ip_list = {}
    server_ip = ''
    for packet in packets:
        if IP in packet:
            if "192.168" not in packet[IP].src:
                server_ip = packet[IP].src
                break
            
            # if packet[IP].src in ip_list:
            #     ip_list[packet[IP].src] = ip_list[packet[IP].src] + 1
            # else:
            #     ip_list[packet[IP].src] = 1
    
    # server_ip = max(ip_list,key=ip_list.get)
    # if "192.168" in server_ip:
    #     del ip_list[server_ip]
    #     server_ip = max(ip_list,key=ip_list.get)

    print("Packet IP is " + server_ip)
    return server_ip

def duration(packets, server_ip):
    # timestamp 값을 이용해서 이전 패킷과의 시간 간격을 계산하고 이를 duration으로 사용
    duration_list = []
    time_list = []

    for i in range(len(packets)):
        if IP in packets[i]:
            if server_ip == packets[i][IP].src or server_ip == packets[i][IP].dst:
                duration_list.append(packets[i].time)
    k = duration_list[0]

    time_list = [f"{i - k:.6f}" for i in duration_list]
    
    print(len(time_list))
    return time_list

def tx_byte(packets, server_ip):

    tx_bytes = []

    for packet in packets:
        if IP in packet:
            if server_ip == packet[IP].src or server_ip == packet[IP].dst:
                if "192.168" in packet[IP].src:
                    tx_byte = len(packet)
                else:
                    tx_byte = -len(packet)
                tx_bytes.append(tx_byte)
    print(len(tx_bytes))
    return tx_bytes

def uplink(packets, server_ip):
    up_packets = []
    for packet in packets:
        if IP in packet:
            if server_ip == packet[IP].src or server_ip == packet[IP].dst:
                if "192.168" in packet[IP].src:
                    up_packets.append(packet)
    return up_packets

def downlink(packets, server_ip):
    down_packets = []
    for packet in packets:
        if IP in packet:
            if server_ip == packet[IP].src or server_ip == packet[IP].dst:
                if "192.168" in packet[IP].dest:
                    down_packets.append(packet)
    return down_packets

def feature_vector(arr):
    res = []
    res.append(max(arr))
    res.append(min(arr))
    res.append(np.mean(arr))
    res.append(np.median(np.absolute(data-np.median(data,axis=0)), axis=0)) 
    res.append(np.std(arr))
    res.append(np.var(arr))
    res.append(skew(arr))
    res.append(kurtosis(arr, fisher=True))
    res.extend(np.percentile(arr, [10,20,30,40,50,60,70,80,90], interpolation='nearest'))
    res.append(len(arr))

    return res


if __name__ == '__main__':
    with open('label_result.txt') as f:
        labels = f.readlines()
        for label in labels:
            res = label.split(', ')

            if len(res) != 2:
                continue
            url, result = res
            if 'facebook' in result:
                url = url[:-5]
                print(url)
                # ip = socket.gethostbyname(url)
                # print("URL IP is " + ip)
                try:
                    packets = rdpcap('traffic/%s.pcap'%(url))

                    server_ip = find_server(packets)

                    up_packets =  uplink(packets, server_ip)
                    down_packets = downlink(packets, server_ip)

                    time_arr = duration(packets, server_ip)
                    down_time_arr = duration(down_packets, server_ip)
                    up_time_arr = duration(up_packets, server_ip)

                    packet_length_arr = tx_byte(packets, server_ip)
                    down_packet_length_arr = tx_byte(down_packets, server_ip)
                    up_packet_length_arr = tx_byte(up_packets, server_ip)
                    
                    data = feature_vector[time_arr] + feature_vector[down_time_arr] + feature_vector[up_time_arr]
                    data += feature_vector[packet_length_arr] + feature_vector[down_packet_length_arr] + feature_vector[up_packet_length_arr]

                    df = pd.DataFrame(data)
                    df.to_csv("parse/%s.csv"%(url), index=None)
                except:
                    print("Error")

        
    