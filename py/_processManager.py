# -*- coding: utf-8 -*-
import time
import multiprocessing as mp

'''
多进程的管理
'''
def do(n):
    time.sleep(n)
    return n*n


class StrategyError(Exception):
    def __init__(self, info):
        super(StrategyError, self).__init__()
        self.info = info

    def __repr__(self):
        return self.info


class ProcessManager(object):
    def __init__(self):
        self._processes = {}
        self._flag = None

    def put(self, worker, name, args):
        self._processes[name] = mp.Process(name=name, target=worker, args=args)

    def start(self, name, background=True, daemon=True):
        worker = self._processes.get(name, '')
        if not worker:
            raise StrategyError('stg not find!')
        worker.daemon = background
        worker.start()
        self._flag = 0
        #print "{name} starting...".format(name=name)
        if daemon:
            self._daemon()
        self._processes[name] = worker

    def stop(self, name):
        worker = self._processes.get(name, '')
        if not worker:
            raise StrategyError('stg not find!')

        if worker.pid is None:
            self._flag = None

        if worker.is_alive():
            worker.terminate()
            time.sleep(0.1)
            self._flag = -1


    def status(self, name):
        worker = self._processes.get(name, '')
        if not worker:
            raise StrategyError('stg not find!')

        if self._flag == 0:
            return worker.pid

        return -1

    def _daemon(self):
        for name, worker in self._processes.items():
            if self._processes[name].is_alive():
                self._processes[name].join()


def test():
    manager = ProcessManager()
    manager.put(worker=do, name='do1', args=(5,))
    manager.put(worker=do, name='do2', args=(3,))
    now = int(time.time())
    manager.start(name='do1')
    manager.start(name='do2')
    print manager.status(name='do1')
    print manager.status(name='do2')
    print int(time.time()) - now

if __name__ == '__main__':
    test()
