from dang_spider import dangdang_ertong,dangdang_teach

import time
import threading

def start_ertong():
    while True:
        start=dangdang_ertong.data_dang()
        start.dangdang()
        time.sleep(3600)

def start_teach():
    while True:
        start=dangdang_teach.data_dang()
        start.dangdang()
        time.sleep(3600)

threads=[]
t1=threading.Thread(target=start_ertong())
threads.append(t1)
t2=threading.Thread(target=start_teach())
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        if t.isAlive( )== False:
            t.start()