# -*- coding: gbk -*-
from config import comicBaseURL, threadCount
from HTMLHandler import getComicInfo
from downloader import Downloader, mutex, picList

if __name__ == "__main__":
    comicId = input("����������ţ�")
    comicURL = comicBaseURL + str(comicId)

    for i in range(threadCount):
        t = Downloader()
        t.start()

    getComicInfo(comicURL)
    Downloader.isStop = True
