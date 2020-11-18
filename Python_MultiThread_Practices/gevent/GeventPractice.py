# -*- coding: utf-8 -*-

from gevent import monkey;
monkey.patch_all() # 自动将python的一些标准模块替换成gevent框架
import gevent
import time
import requests


def req_(url):
    '''

    Args:
        url: 单次get请求的url

    Returns:
        status_code: HTTP响应内容
    '''
    try:
        resp = requests.get(url=url, timeout=10)
        # print(resp.text)
    except Exception as e:
        print(e)


def gevent_(urls):
    '''gevent的封装方法
    Args:
        urls: 执行并发任务的参数列表

    Returns:
    '''
    jobs = [gevent.spawn(req_, url) for url in urls]
    gevent.joinall(jobs, timeout=10)
    for job in jobs:
        job.join()

if __name__ == "__main__":
    TEST_TIMES = 50
    URL = "http://bing.com/"
    urls = [URL] * TEST_TIMES  # 声明重复元素一种方式, 类似的有["https://www.bing.com/" for i in range(10)]
    t1 = time.time()
    gevent_(urls)
    t2 = time.time()
    print('gevent-time:%s' % str(t2 - t1))

    # 分次请求
    t3 = time.time()
    for i in range(TEST_TIMES):
        req_(URL)
    t4 = time.time()
    print('serail-time:%s' % (t4 - t3))
    print("gevent %2f faster than serial req" % (float(t4-t3)/float(t2-t1)))