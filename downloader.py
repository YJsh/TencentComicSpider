# -*- coding: gbk -*-
import os
import time
import threading
import urllib

from config import interval
from utils import mutex, picList

class Downloader(threading.Thread):
    isStop = False

    def downloadPic(self, picURL, picDir, picIndex):
        picPath = os.path.join(picDir, "{0}.jpg".format(picIndex))
        urllib.urlretrieve(picURL, picPath, None) 

    def run(self):
        while True:
            time.sleep(interval)
            mutex.acquire(1)
            if picList != []:
                picURL, picDir, picIndex = picList.pop(0)
            else:
                picURL = ""
            mutex.release()
            if picURL != "":
                self.downloadPic(picURL, picDir, picIndex)
                try:
                    msg = self.name + " succ" + picDir + str(picIndex)
                    print msg
                except:
                    pass
            elif Downloader.isStop:
                break
