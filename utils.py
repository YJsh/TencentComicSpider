# -*- coding: gbk -*-
import os
import re
import threading

def dealWithSpecialCharacter(string, characters="\\/:*?\"<>|", substitute=" "):
    if "\"" in characters:
        string = string.replace("\"", "'")
    pattern = re.compile(r"[%s]"%characters)
    string = pattern.sub(substitute, string)
    return string

def mkdir(*path):
    path = eval("os.path.join(%s)"%str(path)[1:-1])
    if not os.path.exists(path):
        os.mkdir(path)
    return path

mutex = threading.Lock()
picList = []
