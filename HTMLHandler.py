# -*- coding: gbk -*-
import json
import os
import re
import time
import urllib2

from config import *
from utils import dealWithSpecialCharacter, mutex, picList

def handleChapterInfo(data):
    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    def UTF8Decode(c):
        a = ""
        b = d = c1 = c2 = 0
        while b < len(c):
            d = ord(c[b])
            if 128 > d:
                a += chr(d)
                b += 1
            elif 191 < d and 224 > d:
                c2 = ord(c[b+1])
                a += chr((d & 31) << 6 | c2 & 63)
                b += 2
            else:
                c2 = ord(c[b+1])
                c3 = ord(c[b+2])
                a += chr((d & 15) << 12 | (c2 & 63) << 6 | c3 & 63)
                b += 3
        return a

    def decode(c):
        a = ""
        b = d = h = f = g = e = 0
        c = re.sub(r"[^\w\+\/\=]", "", c)
        while e < len(c):
            b = keyStr.index(c[e])
            d = keyStr.index(c[e+1])
            f = keyStr.index(c[e+2])
            g = keyStr.index(c[e+3])
            e = e + 4
            b = b << 2 | d >> 4
            d = (d & 15) << 4 | f >> 2
            h = (f & 3) << 6 | g
            a += chr(b)
            if 64 != f:
                a += chr(d)
            if 64 != g:
                a += chr(h)
        return UTF8Decode(a)
    
    return decode(data[1:])

# ��ȡ�½�ͼƬ����
def getChapterInfo(chapterURL, comicTitle):
    try:
        response = urllib2.urlopen(baseURL + chapterURL)
        print(baseURL + chapterURL)
        content = response.read().decode("utf-8")
    except Exception, e:
        print(e)
        content = ""

    dataPattern = re.compile(
            r"var\s+DATA\s+=\s+'(?P<data>\S+)'")
    data = dataPattern.search(content).group("data")
    chapterInfo = json.loads(handleChapterInfo(data))
    chapterTitle = chapterInfo["chapter"]["cTitle"]
    chapterTitle = dealWithSpecialCharacter(chapterTitle)
    chapterDirPath = os.path.join(baseDirPath, comicTitle, chapterTitle)
    if not os.path.exists(chapterDirPath):
        os.mkdir(chapterDirPath)
    
    mutex.acquire()
    picIndex = 0
    for picInfo in chapterInfo["picture"]:
        picIndex += 1
        picList.append((picInfo["url"], chapterDirPath, picIndex))
    mutex.release()
    
    try:
        print(chapterTitle)
    except:
        pass

def getComicInfo(comicURL):
    try:
        response = urllib2.urlopen(comicURL)
        content = response.read().decode("utf-8")
    except Exception, e:
        print(e)
        return "", []

    comicTitlePattern = re.compile(
            r"<h2 class=\"works-intro-title ui-left\"><strong>(?P<comicTitle>.*?)</strong></h2>")
    result = comicTitlePattern.search(content)
    if not result:
        print("δ�ҵ��������⣬��ȷ�ϣ�")
        return
    comicTitle = result.group("comicTitle")
    comicTitle = dealWithSpecialCharacter(comicTitle)
    print(comicTitle)

    comicChapterPattern = re.compile(
            r"<a target=\"_blank\".*?href=\"(?P<URL>[/\w]+)\">\s")    #����
    chapterURLs = comicChapterPattern.findall(content)
    if not chapterURLs:
        print("δ�ҵ�����½����ӣ���ȷ�ϣ�")
        return
    comicDirPath = os.path.join(baseDirPath, comicTitle)
    if not os.path.exists(comicDirPath):
        os.mkdir(comicDirPath)

    for url in chapterURLs:
        getChapterInfo(url, comicTitle)
        time.sleep(1)
    return comicTitle, chapterURLs

