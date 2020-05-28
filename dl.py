import os
import time
from queue import Queue
import json
from threading import Thread


with open('imgs.json') as f:
    imgs = json.load(f)
img_q = Queue(maxsize=10000000)
for img in imgs:
    img_q.put(img)


def dl():
    while not img_q.empty():
        img = img_q.get()
        os.system(f'wget {img}')


ts = [Thread(target=dl) for _ in range(20)]
for i in ts:
    i.start()
for i in ts:
    i.join()

pics = os.listdir()
data = {
    'time': int(time.time()),
    'count': }
