# coding: utf-8
import re
import time

def isNumber(str):
    isNum = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    if isNum.match(str) or str.isdigit():
        return True
    return False

def transtime(arg, format="%Y-%m-%d %H:%M:%S"):
    if isinstance(arg, int):
        return time.strftime(format, time.localtime(arg))
    elif isinstance(arg, str):
        return int(time.mktime(time.strptime(arg, format)))

if __name__ == '__main__':
    result = isNumber('120.00')
    print(result)
