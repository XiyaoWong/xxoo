import requests
import json
from queue import Queue
from lxml import etree
from threading import Thread
from timeout_decorator import timeout

with open('links.json') as f:
    links = json.load(f)  # type: list

links_queue = Queue(maxsize=10000000)
for link in links:
    links_queue.put(link)

img_queue = Queue(maxsize=10000000)


def get_img():
    while not links_queue.empty():
        link = links_queue.get()
        print('link -> ', link)
        try:
            rep = requests.get(link, timeout=19)
            print(rep.status_code)
            if rep.status_code == 200:
                tree = etree.HTML(rep.text)
                imgs = tree.xpath("//img/@data-original")
                for img in imgs:
                    print('Puted ->', img)
                    img_queue.put(img)
                with open('imgs.json', 'w') as f:
                    json.dump(list(img_queue.queue), f)
        except Exception:
            print('link failed.. -> ', link)
            pass


ts = [Thread(target=get_img) for _ in range(15)]
for t in ts:
    t.start()
for t in ts:
    t.join()

with open('imgs.json', 'w') as f:
    json.dump(list(img_queue.queue), f)
