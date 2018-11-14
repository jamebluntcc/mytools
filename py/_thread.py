# -*- coding: utf-8 -*-
import time
import threading

class myThread(threading.Thread):
    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(self.args)


def func():
    time.sleep(1)
    return None

def main():
    t = myThread(func, (,))
    t.start()
    t.join()

if __name__ == '__main__':
    main()
