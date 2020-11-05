#!/usr/bin/env python
#encoding=utf-8
# author:Unc1e

'''Sleep-based Sql Injection Exploit script, SQL延时注入脚本

延时判断基于requests的超时异常的处理, 更多exception, 见https://cn.python-requests.org/zh_CN/latest/api.html#id3

此外, 在基于页面差异的布尔盲注中, 是否否出现指定关键词, 可用以下几种方法
        1' string.count(),  返回 str 在 string 里面出现的次数
        2' string.find(), 检测 str 是否包含在 string 中，如果是返回第一个值的索引值(从0开始)，否则返回-1
        3' if (symbol_string in string) , 返回布尔值 
'''

import requests 



url = ""
VERIFY = False

# 基于时间的盲注 参数配置
req_url = "" 
TIMEOUT = 8     # 超时时间
AND_MASK_SET = ['1000000','01000000','00100000','00010000','00001000','00000100','00000010','00000001']

def doubleSearch():
    '''
    用8次请求, 确定一位字符的ASCII码
    '''
    pass


for i in range(1, 20):
    try:
        resp = requests.get(url=url, timeout=TIMEOUT, verify=VERIFY)
        if resp.text.count(symbol_string) > 0:#  找到了
            # do process
            pass
        
        else:# 未找到
            continue

    except requests.Timeout:
        # 如果超时
        pass



