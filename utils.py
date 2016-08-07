# -*- coding: gbk -*-
import re
import threading

def dealWithSpecialCharacter(string, characters="\\/:*?\"<>|", substitute=" "):
    if "\"" in characters:
        string = string.replace("\"", "'")
    pattern = re.compile(r"[%s]"%characters)
    string = pattern.sub(substitute, string)
    return string

mutex = threading.Lock()
picList = []
