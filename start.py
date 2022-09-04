#!/usr/bin/env python
# -*- coding:utf-8 -*-
############################################
# File Name    : start.py
# Created By   : Suluo - sampson.suluo@gmail.com
# Creation Date: 2017-12-11
# Last Modified: 2017-12-11 11:30:53
# Descption    :
# Version      : Python 2.7
############################################
import logging
import argparse
import urllib
import urllib2


logger = logging.getLogger(__file__)


def main(num):
    # 启动爬虫
    test_data = {'project':'baidu', 'spider':'baidu'}
    test_data_urlencode = urllib.urlencode(test_data)

    requrl = "http://localhost:6800/schedule.json"

    # 以下是post请求
    req = urllib2.Request(url=requrl, data=test_data_urlencode)

    res_data = urllib2.urlopen(req)
    res = res_data.read()  # res 是str类型
    print(res)

    # 查看日志
    # 以下是get请求
    myproject = "baidu"
    requrl = "http://localhost:6800/listjobs.json?project=" + myproject
    req = urllib2.Request(requrl)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--num', type=int, default=100, help='demo input num')
    args = parser.parse_args()
    main(args.num)


