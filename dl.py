import json
import os
import os.path as op
import time
from queue import Queue
from threading import Thread

if not op.exists('pics'):
    os.mkdir('pics')

with open('imgs.json') as f:
    imgs = json.load(f)
img_q = Queue(maxsize=10000000)
for img in imgs:
    img_q.put(img)


def dl():
    while not img_q.empty():
        img = img_q.get()
        os.system(f'wget -P ./pics {img}')


try:
    ts = [Thread(target=dl) for _ in range(100)]
    for i in ts:
        i.start()
    for i in ts:
        i.join()
except Exception as e:
    print()
    print(e)
    print()
finally:
    pics = os.listdir('pics')
    data = {
        'time': int(time.time()),
        'count': len(pics),
        'pics': pics
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)
