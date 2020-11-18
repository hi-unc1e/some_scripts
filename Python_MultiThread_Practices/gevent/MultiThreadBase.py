# -*- coding: utf-8 -*-

from gevent import monkey;monkey.patch_all()
import gevent
import time
import threading
import requests


def req_(url):
    try:
        requests.get(url=url, timeout=10)
    except Exception as e:
        print(e)


def gevent_(urls):
    jobs = [gevent.spawn(req_, url) for url in urls]
    gevent.joinall(jobs, timeout=10)
    for i in jobs:
        i.join()


def thread_(urls):
    a = []
    for url in urls:
        t = threading.Thread(target=req_, args=(url,))
        a.append(t)

    for i in a:
        i.start()
    for i in a:
        i.join()


if __name__ == "__main__":
    urls = ["https://blog.csdn.net/qq_41874930/article/details/108994480"] * 1000   # 声明重复元素一种方式, 类似的有["https://www.bing.com/" for i in range(10)]
    t1 = time.time()
    gevent_(urls)
    t2 = time.time()
    print('gevent-time:%s' % str(t2 - t1))
    thread_(urls)
    t4 = time.time()
    print('thread-time:%s' % str(t4 - t2))
