# -*- coding:utf-8 -*-
# Author : unc1e, unc1e.com@pm.me
# Data : 2020/11/25 22:44

from gevent import monkey;monkey.patch_all()
import gevent
import requests
import re
import time
import logging


# 下载配置
SAVE_PATH = "E:\\Documents\\HackInn\\"
# SAVE_PATH = "/opt/hackinn/"

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(SAVE_PATH+"log/log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 请求配置
downloadUrl = "https://www.hackinn.com/index.php/archives/{id}/"
ID_Start = 1
ID_End   = 750
SSL_VERIFY = True
TIMEOUT = 8
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 gjdd',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Upgrade-Insecure-Requests": "1",
            }


def appendValidResponse(url):
    '''
    检验response是否为有效响应, 即满足:
    1. 内容不含"404 - 页面没找到"
    2. 响应码是200
    '''
    global Firm_Urls
    xresp = requests.get(url=url, headers=HEADERS, timeout=TIMEOUT, verify=SSL_VERIFY)
    respText = xresp.text
    respCode = xresp.status_code
    NOPE_STRING = "404 - 页面没找到"
    # isValid = False
    if (NOPE_STRING not in respText) and (respCode == 200):
        # isValid = True
        Firm_Urls.append(url)
        msg = ("[+]" + url)
        logger.info(msg)
    time.sleep(5)
    # return isValid


def ExtractDownUrlsByGET(url):
    '''

    '''
    global matchedPDF_Urls
    respText = requests.get(url=url, headers=HEADERS, timeout=TIMEOUT, verify=SSL_VERIFY).text
    # <h2 id="h2--ctf-"><a name="从现实世界到CTF的智能合约攻防" class="reference-link"></a><span class="header-link octicon octicon-link"></span><a href="https://data.hackinn.com/ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.pdf">从现实世界到CTF的智能合约攻防</a></h2>
    matched_U = re.findall(r'''</span><a href="https://data.hackinn.com(.+?)pdf">''', respText) # /ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.
    for u in matched_U:
        tmp = "https://data.hackinn.com{}pdf".format(u)
        matchedPDF_Urls.append(tmp)
    logger.info(matchedPDF_Urls)
    time.sleep(3)
    return matchedPDF_Urls


def DownloadPDFByGET(url):
    '''

    '''
    r = requests.get(url=url, headers=HEADERS, timeout=TIMEOUT, verify=SSL_VERIFY, stream=True)
    # <h2 id="h2--ctf-"><a name="从现实世界到CTF的智能合约攻防" class="reference-link"></a><span class="header-link octicon octicon-link"></span><a href="https://data.hackinn.com/ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.pdf">从现实世界到CTF的智能合约攻防</a></h2>
    filename = url.lstrip("https://data.hackinn.com/ppt/").rstrip().replace("/", "_")  # 2020HACKINGDAY杭州站_从现实世界到CTF的智能合约攻防.pdf
    abs_filepath =  SAVE_PATH + filename
    ALL = 0
    with open(abs_filepath,'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
                # 显示进度
                ALL+=len(chunk)
                print(ALL)
                time.sleep(0.005)
    print("[+]%s downloaded" % filename)

if __name__ == "__main__":
    # time.sleep(100)
    # 先多线程确定存活链接
    possible_Urls = [downloadUrl.format(id=i) for i in range(ID_Start, ID_End)]
    Firm_Urls = []
    # jobs=[gevent.spawn(appendValidResponse, url) for url in possible_Urls]
    # gevent.joinall(jobs)
    for url in possible_Urls:
        appendValidResponse(url)
    print("[+]存活链接数:{}".format(len(Firm_Urls)))
    logger.debug("[+]存活链接数:{}".format(len(Firm_Urls)))
    # 再多线程访问出链接中的PDF链接
    matchedPDF_Urls = []
    jobs=[gevent.spawn(ExtractDownUrlsByGET, url) for url in Firm_Urls]
    gevent.joinall(jobs)
    print("[+]可能有效的PDF数:{}".format(len(matchedPDF_Urls)))
    logger.debug("[+]可能有效的PDF数:{}".format(len(matchedPDF_Urls)))

    # 最后, 多线程下载PDF到指定路径
    jobs=[gevent.spawn(DownloadPDFByGET, url) for url in matchedPDF_Urls]
    gevent.joinall(jobs)




