#!/usr/bin/env python
# -*- coding:utf-8 -*-
############################################
# File Name    : verify.py
# Created By   : Suluo - sampson.suluo@gmail.com
# Creation Date: 2017-12-12
# Last Modified: 2017-12-12 01:55:27
# Descption    :
# Version      : Python3
############################################
from pymongo import MongoClient
import argparse
import requests
import telnetlib
import IPy
import ipaddress
from fake_useragent import UserAgent


def request_verify(address, url="http://www.baidu.com", timeout=10):
    """address = http://218.29.236.50:3128"""
    protocol = address.split("://")[0]
    proxies = {protocol: address}
    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random, "Connection": "close"}
    try:
        res = requests.get(url=url, proxies=proxies, headers=headers, timeout=timeout)
        if str(res.status_code).startswith("20"):
            return True
        else:
            res.raise_for_status()  # 如果响应状态码不是200,主动抛出异常
    except:
        return False


def ipv4network(ip):
    try:
        ipaddress.IPv4Network(ip)
    except Exception as e:
        print(f'netmask is invalid for IPv4: {ip}')
        return False
    return True


def telnet_verify(address, timeout=10):
    """ip = http://218.29.236.50:3128"""
    ip_port = address.split('://')[1]
    ip = ip_port.split(":")[0]
    port = ip_port.split(':')[1]
    try:
        telnetlib.Telnet(host=ip, port=port, timeout=timeout)
    except:
        return False
    else:
        return True


def is_ip(ip):
    """
    https://cloud.tencent.com/developer/article/1355632
    """
    try:
        IPy.IP(ip)
        return True
    except Exception:
        return False


def main(config):
    db = MongoClient(host='127.0.0.1', port=27017).proxy
    for item in db.ip_proxy.find({}, {"_id": 0}):
        if request_verify(item['ipagency']):
            continue
        db.ip_proxy.remove({'_id': item['ipagency']})
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--spider_name', type=str, default="xici", help='spider_name-xici')
    args = parser.parse_args()
    main(args)
