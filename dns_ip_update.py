#!/usr/bin/python
# -*- coding: utf-8 -*-
from QcloudApi.qcloudapi import QcloudApi
import requests
from bs4 import BeautifulSoup
import json
import os
import sys
#get your true IP
def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print('ip:' + ip)
    return ip

def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]

#refer to https://github.com/QcloudApi/qcloudapi-sdk-python
def get_cns_service(secretId,secretKey):
    module = 'cns'
    config = {
        'Region': 'ap-beijing',
        'secretId':secretId,
        'secretKey':secretKey,
        'method': 'get'
    }
    service = QcloudApi(module, config)
    return service

#refers to https://cloud.tencent.com/document/api/302/8517
def get_record_list(cns_service,domain):
    action = 'RecordList'
    params = {
        'domain':domain,
    }
    return cns_service.call(action, params)
#refers to https://cloud.tencent.com/document/api/302/8516
def add_dns_record_ip(cns_service,domain,ip):
    action = 'RecordCreate'
    params = {
        'domain':domain,
        'subDomain':'*',
        'recordLine':'默认',
        'recordType':'A',
        'value':ip,
    }
    return cns_service.call(action,params)

#refers to https://cloud.tencent.com/document/api/302/8511
def modify_dns_record_ip(cns_service,domain,record_id,ip):
    action = 'RecordModify'
    params = {
        'domain':domain,
        'subDomain':'*',
        'recordId':record_id,
        'recordLine':'默认',
        'recordType':'A',
        'value':ip,
    }
    return cns_service.call(action,params)



if (__name__ == '__main__'):
    #Need reqeust in https://console.cloud.tencent.com/capi
    secretId = 'your id'
    secretKey =  'your key'

    #buy domain name in https://dnspod.cloud.tencent.com/?from=qcloudProductDns
    domain = 'your domain name'

    ip = get_out_ip(get_real_url())
    OUT_IP_FILE = './out_ip.txt'

    if not os.path.exists(OUT_IP_FILE):
        with open(OUT_IP_FILE,'w+') as f:
            f.write(ip)
            print("[dns_tool]:Cache IP:{} as file".format(ip))
    else:
        with open(OUT_IP_FILE,'r+') as f:
            old_ip = f.read()
            if old_ip == ip:
                print("[dns_tool]:not need update,current IP:"+old_ip)
                sys.exit(0)

            else:
                f.seek(0)
                f.truncate(0)
                f.write(ip)
                print("[dns_tool]:Update a IP:{},old ip: {}".format(ip,old_ip))

    service = get_cns_service(secretId,secretKey)
    record_list = json.loads(get_record_list(service,domain))

    is_ip = False
    record_id = 0
    for item in record_list["data"]["records"]:
        if item["type"] == 'A':
            is_ip = True
            record_id = item["id"]
            modify_dns_record_ip(service, domain, record_id, ip)
            print("[dns_tool]:Modify a record, id: {}".format(record_id))
    if not is_ip:
        add_dns_record_ip(service, domain,ip)
        print("[dns_tool]:Create a new ip record for domain: "+domain)

    #you can review your IP in https://console.cloud.tencent.com/domain/manage



