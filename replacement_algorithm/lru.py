from .base import *
import collections
import intervals

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
        if self.check(req):
            self.cacheStack.move_to_end(req.id)
            self.hitTimes += 1
            return True
        return False

    def check(self, req:SimpleRequest) -> bool:
        if req.id in self.cacheStack:
            cacheObj = self.cacheStack[req.id]
            reqInterval = intervals.closed(req.start,req.end)
            if reqInterval in cacheObj.interval:
                return True
        return False

    def admit(self,req:SimpleRequest):
        if self.check(req):
            return
        realSize = req.end - req.start +1

        if realSize > self.cacheSize:
            print("Unaccpetable Request Size")
            exit(0)

        uncacheSize = 0
        finalCacheObj = CacheObject(req)

        if req.id in self.cacheStack:
            cacheObj = self.cacheStack[req.id]
            reqInterval = intervals.closed(req.start,req.end)
            finalInterval = cacheObj.interval | reqInterval
            uncacheSize = getIntervalSize(finalInterval) - getIntervalSize(cacheObj.interval)
            finalCacheObj.interval = finalInterval
        else:
            uncacheSize = req.end - req.start + 1

        while uncacheSize+self.currentSize > self.cacheSize :
            self.evict()

        self.originTraffic += uncacheSize
        self.currentSize += uncacheSize

        self.cacheStack[req.id] = finalCacheObj

    def evict(self):
        obj = self.cacheStack.popitem(False)[1]
        self.currentSize -= obj.size

    def statics(self):
        self.hitRatio = self.hitTimes/self.requestTimes

        print("LRU Method:",
              '\n Request Times : ',self.requestTimes,
              '\n Hit Times : ',self.hitTimes,
              '\n Hit Ratio : ',self.hitRatio,
              '\n Origin Traffic : ', self.originTraffic)
