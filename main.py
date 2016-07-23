# -*- coding: utf-8 -*-
import os
import re
import urllib2
import threading

baseDirPath = "./"
baseURL = "http://ac.qq.com/"
comicBaseURL = "http://ac.qq.com/Comic/comicInfo/id/"
comicId = 505430

def dealWithSpecialCharacter(string, characters="\\/:*?\"<>|", substitute=" "):
    if "\"" in characters:
        string = string.replace("\"", "'")
    pattern = re.compile(r"[%s]"%characters)
    string = pattern.sub(substitute, string)
    return string

def downloadImg(imgURL, imgDir, imgIndex):
    imgPath = os.path.join(imgDir, "{0}.jpg".format(imgIndex))
    urllib.urlretrieve(imgURL, imgPath, None) 

def getChapterImgInfo(chapterURL):
    print("getChapterImgInfo")
    try:
        response = urllib2.urlopen(baseURL + chapterURL)
        print(baseURL + chapterURL)
        content = response.read()
    except Exception, e:
        print(e)
        content = ""

    imgPattern = re.compile(
            r"<li style=\"width: 822px; height: 1200px;\">\S+<img src=\"(?P<imgURL>.*)\"")
    imgURLs = imgPattern.findall(content)
    print imgURLs
    

def getComicChapterInfo(comicURL):
    try:
        response = urllib2.urlopen(comicURL)
        content = response.read()
    except Exception, e:
        print(e)
        return "", []

    comicNamePattern = re.compile(
            r"<h2 class=\"works-intro-title ui-left\"><strong>(?P<comicName>.*?)</strong></h2>")
    result = comicNamePattern.search(content)
    if not result:
        print("未找到漫画标题，请确认！")
        return "", []
    comicName = result.group("comicName").decode("utf-8")
    comicName = dealWithSpecialCharacter(comicName)
    print(comicName)

    comicDirPath = baseDirPath + comicName
    #if not os.path.isabs(comicDirPath):
    #    comicDirPath = os.path.abspath(comicDirPath)
    if not os.path.exists(comicDirPath):
        os.mkdir(comicDirPath)

    comicChapterPattern = re.compile(
            r"<a target=\"_blank\".*?href=\"(?P<URL>[/\w]+)\">\s")    #链接
    chapterURLs = comicChapterPattern.findall(content)
    if not chapterURLs:
        print("未找到相关章节链接，请确认！")
        return comicName, []
    return comicName, chapterURLs

if __name__ == "__main__":
    comicURL = comicBaseURL + str(comicId)
    comicName, chapterURLs = getComicChapterInfo(comicURL)
    getChapterImgInfo(chapterURLs[1])
