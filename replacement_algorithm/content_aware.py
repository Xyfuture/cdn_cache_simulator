from replacement_algorithm.base import *
from replacement_algorithm.lru import lru


class DynamicLRU(lru):
    def __init__(self, cacheSize):
        super().__init__(cacheSize)
        self.time_serises= []

    def changeCacheSize(self, cacheSize):
        while self.currentSize > cacheSize:
            self.evict()
        self.cacheSize = cacheSize

    def lookup(self, req: SimpleRequest) -> bool:
        self.time_serises.append(req)
        return super(DynamicLRU, self).lookup(req)


    def predict(self)->int:
        pass

    def set_config(self):
        pass


class ContentAware(ReplaceAlgo):
    def __init__(self, cacheSize, cfg):
        super().__init__(cacheSize)
        self.contentCache = {}
        self.contentTypes = []

        self.requestTimes = 0
        self.hitTimes = 0
        self.originTraffic = 0
        self.curTime = 0

    def lookup(self, req: SimpleRequest) -> bool:
        self.requestTimes += 1

        if req.time> self.curTime+self.timeInterval:
            self.curTime = req.time
            self.updateSize()

        if self.contentCache[req.type].lookup(req):
            self.hitTimes+=1
            return True
        return False

    # currently not use
    def check(self, id: int, type):
        if self.contentCache[type].check(id):
            return True
        return False

    def admit(self, req: SimpleRequest):
        if self.check(req.id, req.type):
            return
        self.contentCache[req.type].admit(req)
        self.originTraffic += req.size

    def evict(self):
        pass

    # find a time
    def updateSize(self):
        total = 0
        component = {}
        for k,v in self.contentCache.items():
            component[k] = v.predict()
            total += component[k]
        for k,v in component.items():
            cur = v/total
            self.contentCache[k].changeCacheSize(cur*self.cacheSize)

    def set_config(self):
        pass