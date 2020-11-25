# -*- coding:utf-8 -*-
# Author : unc1e, unc1e.com@pm.me
# Data : 2020/11/25 22:44

from gevent import monkey,pool
monkey.patch_all()
import gevent
import requests
import re
import time
import logging


# TODO
# 下载时数据的持久化，例如有多少有效链接，不要每次都自己爬取， 考虑mysql/txt/redis
# 下载进度查看

# 下载配置
SAVE_PATH = "E:\\Documents\\HackInn\\"
# SAVE_PATH = "/opt/hackinn/"

# 日志配置
# logger = logging.getLogger(__name__)
# logger.setLevel(level = logging.INFO)
# handler = logging.FileHandler(SAVE_PATH+"log/log.txt")
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# 请求配置
downloadUrl = "https://www.hackinn.com/index.php/archives/{id}/"
ID_Start = 1
ID_End   = 750
SSL_VERIFY = True
TIMEOUT = 8
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 gjdd',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Upgrade-Insecure-Requests": "1"
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
        print(msg)
#         # logger.info(msg)
    # return isValid


def ExtractDownUrlsByGET(url):
    '''

    '''
    global matchedPDF_Urls
    respText = requests.get(url=url, headers=HEADERS, timeout=TIMEOUT, verify=SSL_VERIFY).text
    # <h2 id="h2--ctf-"><a name="从现实世界到CTF的智能合约攻防" class="reference-link"></a><span class="header-link octicon octicon-link"></span><a href="https://data.hackinn.com/ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.pdf">从现实世界到CTF的智能合约攻防</a></h2>
    matched_U = re.findall('''https://data.hackinn.com/ppt/(.+?)pdf''', respText) # /ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.
    for u in matched_U:
        tmp = "https://data.hackinn.com/ppt/{}pdf".format(u)
        matchedPDF_Urls.append(tmp)

    # logger.info(matchedPDF_Urls)
    # gevent.sleep(10)
    print(len(matchedPDF_Urls))


def DownloadPDFByGET(url):
    '''
    3678份PPT，未去重
    '''
    r = requests.get(url=url, headers=HEADERS, timeout=TIMEOUT, verify=SSL_VERIFY, stream=True)
    # <h2 id="h2--ctf-"><a name="从现实世界到CTF的智能合约攻防" class="reference-link"></a><span class="header-link octicon octicon-link"></span><a href="https://data.hackinn.com/ppt/2020HACKINGDAY杭州站/从现实世界到CTF的智能合约攻防.pdf">从现实世界到CTF的智能合约攻防</a></h2>
    filename = url.lstrip("https://data.hackinn.com/ppt/").rstrip().replace("/", "_").replace("%20", "_")    # 2020HACKINGDAY杭州站_从现实世界到CTF的智能合约攻防.pdf
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
    p = pool.Pool(5)

    # time.sleep(100)
    # 先多线程确定存活链接
    # possible_Urls = [downloadUrl.format(id=i) for i in range(ID_Start, ID_End)]
    # Firm_Urls = []
    # jobs=[p.spawn(appendValidResponse, url) for url in possible_Urls]
    # gevent.joinall(jobs)
    # for url in possible_Urls:
    #     appendValidResponse(url)
    # print("[+]存活链接数:{}".format(len(Firm_Urls)))
    # logger.debug("[+]存活链接数:{}".format(len(Firm_Urls)))
    # 再多线程访问出链接中的PDF链接
    Firm_Urls = ["https://www.hackinn.com/index.php/archives/16/","https://www.hackinn.com/index.php/archives/32/","https://www.hackinn.com/index.php/archives/38/","https://www.hackinn.com/index.php/archives/43/","https://www.hackinn.com/index.php/archives/60/","https://www.hackinn.com/index.php/archives/62/","https://www.hackinn.com/index.php/archives/70/","https://www.hackinn.com/index.php/archives/74/","https://www.hackinn.com/index.php/archives/77/","https://www.hackinn.com/index.php/archives/82/","https://www.hackinn.com/index.php/archives/85/","https://www.hackinn.com/index.php/archives/89/","https://www.hackinn.com/index.php/archives/96/","https://www.hackinn.com/index.php/archives/99/","https://www.hackinn.com/index.php/archives/103/","https://www.hackinn.com/index.php/archives/112/","https://www.hackinn.com/index.php/archives/116/","https://www.hackinn.com/index.php/archives/136/","https://www.hackinn.com/index.php/archives/137/","https://www.hackinn.com/index.php/archives/141/","https://www.hackinn.com/index.php/archives/146/","https://www.hackinn.com/index.php/archives/149/","https://www.hackinn.com/index.php/archives/170/","https://www.hackinn.com/index.php/archives/182/","https://www.hackinn.com/index.php/archives/187/","https://www.hackinn.com/index.php/archives/188/","https://www.hackinn.com/index.php/archives/190/","https://www.hackinn.com/index.php/archives/191/","https://www.hackinn.com/index.php/archives/194/","https://www.hackinn.com/index.php/archives/196/","https://www.hackinn.com/index.php/archives/197/","https://www.hackinn.com/index.php/archives/199/","https://www.hackinn.com/index.php/archives/212/","https://www.hackinn.com/index.php/archives/220/","https://www.hackinn.com/index.php/archives/221/","https://www.hackinn.com/index.php/archives/222/","https://www.hackinn.com/index.php/archives/225/","https://www.hackinn.com/index.php/archives/231/","https://www.hackinn.com/index.php/archives/234/","https://www.hackinn.com/index.php/archives/238/","https://www.hackinn.com/index.php/archives/246/","https://www.hackinn.com/index.php/archives/264/","https://www.hackinn.com/index.php/archives/267/","https://www.hackinn.com/index.php/archives/268/","https://www.hackinn.com/index.php/archives/270/","https://www.hackinn.com/index.php/archives/272/","https://www.hackinn.com/index.php/archives/277/","https://www.hackinn.com/index.php/archives/278/","https://www.hackinn.com/index.php/archives/279/","https://www.hackinn.com/index.php/archives/283/","https://www.hackinn.com/index.php/archives/294/","https://www.hackinn.com/index.php/archives/299/","https://www.hackinn.com/index.php/archives/333/","https://www.hackinn.com/index.php/archives/334/","https://www.hackinn.com/index.php/archives/337/","https://www.hackinn.com/index.php/archives/346/","https://www.hackinn.com/index.php/archives/352/","https://www.hackinn.com/index.php/archives/357/","https://www.hackinn.com/index.php/archives/360/","https://www.hackinn.com/index.php/archives/362/","https://www.hackinn.com/index.php/archives/366/","https://www.hackinn.com/index.php/archives/368/","https://www.hackinn.com/index.php/archives/372/","https://www.hackinn.com/index.php/archives/375/","https://www.hackinn.com/index.php/archives/376/","https://www.hackinn.com/index.php/archives/377/","https://www.hackinn.com/index.php/archives/378/","https://www.hackinn.com/index.php/archives/382/","https://www.hackinn.com/index.php/archives/393/","https://www.hackinn.com/index.php/archives/394/","https://www.hackinn.com/index.php/archives/396/","https://www.hackinn.com/index.php/archives/438/","https://www.hackinn.com/index.php/archives/441/","https://www.hackinn.com/index.php/archives/443/","https://www.hackinn.com/index.php/archives/447/","https://www.hackinn.com/index.php/archives/452/","https://www.hackinn.com/index.php/archives/455/","https://www.hackinn.com/index.php/archives/456/","https://www.hackinn.com/index.php/archives/462/","https://www.hackinn.com/index.php/archives/465/","https://www.hackinn.com/index.php/archives/467/","https://www.hackinn.com/index.php/archives/469/","https://www.hackinn.com/index.php/archives/471/","https://www.hackinn.com/index.php/archives/472/","https://www.hackinn.com/index.php/archives/473/","https://www.hackinn.com/index.php/archives/476/","https://www.hackinn.com/index.php/archives/478/","https://www.hackinn.com/index.php/archives/480/","https://www.hackinn.com/index.php/archives/483/","https://www.hackinn.com/index.php/archives/484/","https://www.hackinn.com/index.php/archives/486/","https://www.hackinn.com/index.php/archives/487/","https://www.hackinn.com/index.php/archives/488/","https://www.hackinn.com/index.php/archives/489/","https://www.hackinn.com/index.php/archives/490/","https://www.hackinn.com/index.php/archives/492/","https://www.hackinn.com/index.php/archives/498/","https://www.hackinn.com/index.php/archives/500/","https://www.hackinn.com/index.php/archives/501/","https://www.hackinn.com/index.php/archives/502/","https://www.hackinn.com/index.php/archives/505/","https://www.hackinn.com/index.php/archives/507/","https://www.hackinn.com/index.php/archives/508/","https://www.hackinn.com/index.php/archives/510/","https://www.hackinn.com/index.php/archives/512/","https://www.hackinn.com/index.php/archives/514/","https://www.hackinn.com/index.php/archives/515/","https://www.hackinn.com/index.php/archives/516/","https://www.hackinn.com/index.php/archives/517/","https://www.hackinn.com/index.php/archives/518/","https://www.hackinn.com/index.php/archives/519/","https://www.hackinn.com/index.php/archives/520/","https://www.hackinn.com/index.php/archives/531/","https://www.hackinn.com/index.php/archives/540/","https://www.hackinn.com/index.php/archives/557/","https://www.hackinn.com/index.php/archives/558/","https://www.hackinn.com/index.php/archives/559/","https://www.hackinn.com/index.php/archives/560/","https://www.hackinn.com/index.php/archives/561/","https://www.hackinn.com/index.php/archives/562/","https://www.hackinn.com/index.php/archives/563/","https://www.hackinn.com/index.php/archives/564/","https://www.hackinn.com/index.php/archives/565/","https://www.hackinn.com/index.php/archives/566/","https://www.hackinn.com/index.php/archives/567/","https://www.hackinn.com/index.php/archives/568/","https://www.hackinn.com/index.php/archives/666/","https://www.hackinn.com/index.php/archives/671/","https://www.hackinn.com/index.php/archives/672/","https://www.hackinn.com/index.php/archives/686/","https://www.hackinn.com/index.php/archives/688/","https://www.hackinn.com/index.php/archives/695/","https://www.hackinn.com/index.php/archives/714/","https://www.hackinn.com/index.php/archives/716/","https://www.hackinn.com/index.php/archives/719/","https://www.hackinn.com/index.php/archives/720/","https://www.hackinn.com/index.php/archives/721/","https://www.hackinn.com/index.php/archives/722/","https://www.hackinn.com/index.php/archives/723/","https://www.hackinn.com/index.php/archives/727/","https://www.hackinn.com/index.php/archives/728/","https://www.hackinn.com/index.php/archives/730/","https://www.hackinn.com/index.php/archives/733/","https://www.hackinn.com/index.php/archives/734/","https://www.hackinn.com/index.php/archives/744/"]

    matchedPDF_Urls = []
    jobs=[p.spawn(ExtractDownUrlsByGET, url) for url in Firm_Urls]
    gevent.joinall(jobs)
    # for url in Firm_Urls:
    #     ExtractDownUrlsByGET(url)
    # print("[+]可能有效的PDF数:{}".format(len(matchedPDF_Urls)))
    # logger.debug("[+]可能有效的PDF数:{}".format(len(matchedPDF_Urls)))
    p = pool.Pool(20)
    # 最后, 多线程下载PDF到指定路径
    jobs=[p.spawn(DownloadPDFByGET, url) for url in matchedPDF_Urls]
    gevent.joinall(jobs)




