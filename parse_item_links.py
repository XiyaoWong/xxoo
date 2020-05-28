import requests
import json
from queue import Queue
from lxml import etree
from threading import Thread

all_links = Queue(maxsize=1000)

all_pages = Queue(maxsize=30)
for i in range(1, 26):
    all_pages.put(i)


def get_one():
    while not all_pages.empty():
        page = all_pages.get()
        print('Page -> ', page)
        url = f'http://zazhitaotu.com/page/{page}'
        rep = requests.get(url, timeout=15)
        if rep.status_code == 200:
            tree = etree.HTML(rep.text)
            links = tree.xpath("//a[@class='item-link']/@href")
            for link in links:
                all_links.put(link)
                print('Puted', link)


ts = [Thread(target=get_one) for _ in range(5)]
for t in ts:
    t.start()
for t in ts:
    t.join()

with open('links.json', 'w') as f:
    json.dump(list(all_links.queue), f)
