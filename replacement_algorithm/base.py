from abc import ABCMeta, abstractmethod


class ReplaceAlgo(metaclass=ABCMeta):
    def __init__(self, cacheSize):
        self.cacheSize = cacheSize
        self.currentSize = 0
        pass

    @abstractmethod
    def lookup(self, req):
        pass

    @abstractmethod
    def admit(self, req):
        pass

    @abstractmethod
    def evict(self):
        pass


class SimpleRequest():
    def __init__(self, id, time, size, type):
        self.id = id
        self.time = time
        self.size = size
        self.type = type
        pass

    def print(self):
        pass


class CacheObject():
    def __init__(self, req: SimpleRequest = None):
        if req:
            self.id = req.id
            self.size = req.size
            self.type = req.type
        self.id = -1
        self.size = 0
        self.type = 0


    def print(self):
        pass