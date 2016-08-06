# -*- coding: gbk -*-
import os
import re
import json
import time
import urllib
import urllib2
import threading

baseDirPath = "./"
baseURL = "http://ac.qq.com/"
comicBaseURL = "http://ac.qq.com/Comic/comicInfo/id/"

def dealWithSpecialCharacter(string, characters="\\/:*?\"<>|", substitute=" "):
    if "\"" in characters:
        string = string.replace("\"", "'")
    pattern = re.compile(r"[%s]"%characters)
    string = pattern.sub(substitute, string)
    return string

def downloadPic(picURL, picDir, picIndex):
    picPath = os.path.join(picDir, "{0}.jpg".format(picIndex))
    urllib.urlretrieve(picURL, picPath, None) 

# 获取章节图片数据
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

def getChapterInfo(chapterURL):
    print("getChapterInfo")
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
    chapterDirPath = os.path.join(baseDirPath, comicTitle, chapterTitle)
    if not os.path.exists(chapterDirPath):
        os.mkdir(chapterDirPath)

    picUrls = []
    for picInfo in chapterInfo["picture"]:
        picUrls.append(picInfo["url"])
    print(chapterTitle)
    return chapterTitle, picUrls

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
        print("未找到漫画标题，请确认！")
        return "", []
    comicTitle = result.group("comicTitle")
    comicTitle = dealWithSpecialCharacter(comicTitle)
    print(comicTitle)

    comicChapterPattern = re.compile(
            r"<a target=\"_blank\".*?href=\"(?P<URL>[/\w]+)\">\s")    #链接
    chapterURLs = comicChapterPattern.findall(content)
    if not chapterURLs:
        print("未找到相关章节链接，请确认！")
        return comicTitle, []
    return comicTitle, chapterURLs

if __name__ == "__main__":
    comicId = 505430
    comicId = input("输入漫画编号：")
    comicURL = comicBaseURL + str(comicId)
    comicTitle, chapterURLs = getComicInfo(comicURL)

    comicDirPath = os.path.join(baseDirPath, comicTitle)
    if not os.path.exists(comicDirPath):
        os.mkdir(comicDirPath)

    chapterTitle, picUrls = getChapterInfo(chapterURLs[0])
    picIndex = 1
    picDir = os.path.join(baseDirPath, comicTitle, chapterTitle)
    for url in picUrls:
        downloadPic(url, picDir, picIndex)
        picIndex += 1
        time.sleep(1)
