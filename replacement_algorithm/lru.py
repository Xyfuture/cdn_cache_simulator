from replacement_algorithm.base import *
import collections


class lru(ReplaceAlgo):
    def __init__(self, cacheSize):
        super().__init__(cacheSize)
        self.cacheStack = collections.OrderedDict()

        self.originTraffic = 0
        self.hitTimes = 0
        self.requestTimes = 0
        self.hitRatio = 0

    def lookup(self, req: SimpleRequest) -> bool:
        self.requestTimes += 1
        id = req.id
        if self.check(id):
            self.cacheStack.move_to_end(id)
            self.hitTimes += 1
            return True
        return False

    def check(self, id: int) -> bool:
        if id in self.cacheStack:
            return True
        return False

    def admit(self,req:SimpleRequest):
        if self.check(req.id):
            return
        size = req.size
        if size > self.cacheSize:
            print("Unaccpetable Request Size")
        while size+self.currentSize > self.cacheSize :
            self.evict()
        self.originTraffic += size
        self.currentSize += size

        self.cacheStack[req.id] = CacheObject(req)

    def evict(self):
        obj = self.cacheStack.popitem(False)
        self.currentSize -= obj.size

    def statics(self):
        self.hitRatio = self.hitTimes/self.requestTimes

        print("LRU Method:",
              '\n Request Times : ',self.requestTimes,
              '\n Hit Times : ',self.hitTimes,
              '\n Hit Ratio : ',self.hitRatio,
              '\n Origin Traffic : ', self.originTraffic)
