from abc import ABCMeta, abstractmethod
import intervals

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
    def __init__(self, id, time, size, type,start,end):
        self.id = id
        self.time = time
        self.size = size # full size
        self.type = type

        self.start = start
        self.end = end
        pass

    def checkInterval(self)->bool:
        if self.end >= self.size:
            return  False
        if self.start>=self.end:
            return  False
        if self.start <0 or self.end <0:
            return  False
        return True


    def print(self):
        print(self.__str__())

    def __str__(self):
        _str = "request:\n" \
               "id:{}\n" \
               "type:{}\n" \
               "start:{}  end:{}\n" \
               "size:{}".format(self.id,self.type,self.start,self.end,self.size)
        return _str





class CacheObject():
    def __init__(self, req: SimpleRequest = None):
        if req:
            self.id = req.id
            self.type = req.type
            self.interval = intervals.closed(req.start,req.end)

        else:
            self.id = -1
            self.type = 0
            self.interval = intervals.closed(0,0)

    @property
    def size(self)->int:
        total_size = 0
        for i in self.interval:
            total_size += i.upper-i.lower +1
        return total_size


    def print(self):
        print(self.__str__())

    def __str__(self):
        _str = "cache object:\n" \
               "id:{}\n" \
               "type:{}\n" \
               "interval:{}\n" \
               "real size:{}".format(self.id,self.type,self.interval,self.size)
        return _str



def getIntervalSize(interval:intervals)->int:
    total_size = 0
    for i in interval:
        total_size += i.upper-i.lower+1
    return total_size
