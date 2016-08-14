# -*- coding: gbk -*-
import os
import time
import Tkinter

import utils
from config import *
from downloader import Downloader
from HTMLHandler import getComicInfo, getChapterInfo

class App(object):
    def __init__(self, title):
        self.window      = Tkinter.Tk()
        self.comicId     = Tkinter.StringVar()
        self.comicTitle  = ""
        self.chapterURLs = []

        self.window.title(title)
        self.window.geometry("640x480")

        Tkinter.Label(self.window,text=u"请输入漫画 ID").pack()
        Tkinter.Entry(self.window, textvariable=self.comicId).pack()
        Tkinter.Button(self.window, text=u"确定", command=self.getComicInfo).pack()

    def getComicInfo(self):
        comicURL = comicBaseURL + self.comicId.get()
        self.comicTitle, self.chapterURLs, errMsg = getComicInfo(comicURL)
        if errMsg:
            Tkinter.Label(self.window, text=errMsg).pack()
            return

        Tkinter.Label(self.window, text=self.comicTitle).pack()
        Tkinter.Button(self.window, text=u"全部下载", command=self.downloadAll).pack()

    def downloadAll(self):
        utils.mkdir(baseDirPath, self.comicTitle)
        for i in range(threadCount):
            t = Downloader()
            t.start()
        for url in self.chapterURLs[:2]:
            getChapterInfo(url, self.comicTitle)
            time.sleep(1)
        Downloader.isStop = True
        Tkinter.Label(self.window, text=u"下载完成").pack()

    def run(self):
        self.window.mainloop()

