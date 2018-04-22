# coding: utf-8
import re
def isNumber(str):
    isNum = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    if isNum.match(str) or str.isdigit():
        return True
    return False


if __name__ == '__main__':
    result = isNumber('120.00')
    print(result)