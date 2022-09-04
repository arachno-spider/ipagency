#!/bin/bash
# ====================================================
#   Copyright (C)2020 All rights reserved.
#
#   Author        : sam_suluo
#   Email         : sam_suluo@163.com
#   File Name     : start.sh
#   Last Modified : 2022/9/3 23:03
#   Describe      :
#
# ====================================================
set -x
set -e

pt='2020-12-01'


scrapy crawl kuaidaili

scrapy crawl yundaili
