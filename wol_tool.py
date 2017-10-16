# -*- coding:utf-8 -*-
"""
This code is from internet, not written by me.
@author:Peter
@file:wol_tool.py
@time:2017/10/1610:59
"""

import socket
import struct

def wol(mac,broadcast_ip=None):
    if len(mac) == 17:
        mac = mac.replace(mac[2],'')

    if len(mac) != 12:
        raise ValueError('Invalid Mac address')

    data = 'FFFFFFFFFFFF%s' %(mac*16)
    magic_data = ''
    for i in range(0,len(data),2):
	magic_data = ''.join([magic_data,struct.pack('B',int(data[i:i+2],16))])

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    if not broadcast_ip:broadcast_ip = '255.255.255.255'
    #sock.sendto(magic_data,(broadcast_ip,0))
    sock.sendto(magic_data, (broadcast_ip, 7))
    sock.sendto(magic_data, (broadcast_ip, 9))
    return True

if __name__ == '__main__':
    #change your PC mac.
    wol('1C:1B:0D:3B:01:29')
    exit(0)

