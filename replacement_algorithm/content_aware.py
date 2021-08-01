from .base import *
from .lru import lru
import configparser
import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA


class DynamicLRU(lru):
    def __init__(self, cacheSize=0):
        super().__init__(cacheSize)
        self.time_series= []
        self.current_period = []

    def changeCacheSize(self, cacheSize):
        while self.currentSize > cacheSize:
            self.evict()
        self.cacheSize = cacheSize

    def lookup(self, req: SimpleRequest) -> bool:
        self.current_period.append(req)
        return super(DynamicLRU, self).lookup(req)


    def predict(self)->int:
        if not self.udpateSeries():
            return -1
        self.model.update(self.time_series)
        pre = self.model.predict(n_periods= 1)
        return int(pre[0])

    def udpateSeries(self)->bool:
        if not self.current_period:
            return False
        total_number = 0
        for i in self.current_period:
            total_number += 1
            # if we use size tatal_number += i.size or (i.end-i.start +1 )
        self.current_period = []
        self.time_series.append(total_number)
        return True

    def trainModel(self):
        if not self.time_series:
            print('Lack of time series info')
            exit(0)
        self.model = pm.auto_arima(self.time_series, start_p=1, start_q=1,
                              test='adf',  # use adftest to find optimal 'd'
                              max_p=5, max_q=5,  # maximum p and q
                              m=1,  # frequency of series
                              d=None,  # let model determine 'd'
                              seasonal=False,  # No Seasonality
                              start_P=0,
                              D=0,
                              trace=False,
                              error_action='ignore',
                              suppress_warnings=True,
                              stepwise=True)

    def getModelInfo(self):
        print(self.model.summary())

    # TODO
    # set config we need
    def set_config(self):
        pass


class ContentAware(ReplaceAlgo):
    def __init__(self, cacheSize=0,cfgFileName=None):
        super().__init__(cacheSize)
        self.contentCache = {}
        self.contentTypes = []

        self.requestTimes = 0
        self.hitTimes = 0
        # self.originTraffic = 0
        self.curTime = 0

        self.updateIteration = 0

        if cfgFileName:
            self.set_config(cfgFileName)
        else:
            print("Lack of config file for content aware cache")
            exit(0)


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
    def check(self,req:SimpleRequest):
        if self.contentCache[req.type].check(req):
            return True
        return False

    def admit(self, req: SimpleRequest):
        if self.check(req):
            return
        self.contentCache[req.type].admit(req)
        # self.originTraffic += req.end -req.start + 1

    def evict(self):
        pass

    # find a time
    def updateSize(self):

        self.updateIteration += 1
        if self.updateIteration < self.startIteration:
            for k,v in self.contentCache.items():
                v.udpateSeries()
            return
        elif self.updateIteration == self.startIteration:
            for k,v in self.contentCache.items():
                v.trainModel()

        total = 0
        component = {}
        for k,v in self.contentCache.items():
            component[k] = v.predict()
            total += component[k]
        for k,v in component.items():
            cur = v/total
            self.contentCache[k].changeCacheSize(int(cur*self.cacheSize))

    # TODO
    # add new config settings
    def set_config(self,fileName):
        cfg = configparser.ConfigParser()
        cfg.read(fileName,encoding='utf-8')
        if 'content_aware' in cfg:
            self.contentTypes = cfg['content_aware']['type'].split(' ')
            self.timeInterval = int(cfg['content_aware']['time_interval'])
            self.startIteration = int(cfg['content_aware']['start_iteration'])
            self.initialRatio = [int(i) for i in cfg['content_aware']['initial_ratio'].split(' ')]

            totalRatio = sum(self.initialRatio)
            for k,v in zip(self.contentTypes,self.initialRatio):
                self.contentCache[k] = DynamicLRU(int((v/totalRatio)*self.cacheSize))

        else:
            print('Config doesn\'t have content aware part')
            exit(0)

    @property
    def originTraffic(self):
        traffic = 0
        for k,v in self.contentCache:
            traffic += v.originTraffic
        return traffic

    def statics(self):
        self.hitRatio = self.hitTimes/self.requestTimes

        print("Content-Aware Method:",
              '\n Request Times : ',self.requestTimes,
              '\n Hit Times : ',self.hitTimes,
              '\n Hit Ratio : ',self.hitRatio,
              '\n Origin Traffic : ', self.originTraffic)