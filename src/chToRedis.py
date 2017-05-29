'''
Created on May 28, 2017

@author: acer
'''
from src.satori.websock import readWebsock
import json
from pprint import pprint
from src.cfg import cfg
import time
import redis
class timerForSlotShift ():
#at specified time interval shifts slots (should lock slots while shifting..not done yet)
    def __init__(self,slotShiftInterval,refreshInterval,totalTime):
        super().__init__()
        self.slotShiftInterval=slotShiftInterval
        self.refreshInterval=refreshInterval
        self.timeLeft=totalTime
        self.ns = slotShiftInterval
        self.nr = refreshInterval
        if (self.nr < self.ns):
            self.sleepInterval=self.nr
        else:
            self.sleepInterval=self.ns
    def calcTimeState(self):
        #A short algorithm that supports refresh and slotshift. Keeps the timeout value and
        #the state of the time out -- either slotshift or refresh using two numbers and a state
        self.ns -= self.sleepInterval
        self.nr -= self.sleepInterval
        if (self.ns == 0):
            self.ns = self.slotShiftInterval
        if (self.nr ==0 ):
            self.nr = self.refreshInterval
        if (self.ns > self.nr ):
            self.slotShiftState=False
            self.sleepInterval = self.nr
        else:
            self.slotShiftState=True
            self.sleepInterval = self.ns           
    def slotShift(self):
        #urlString = endpoint + '?appkey='+appkey
        time.sleep(self.sleepInterval)
        self.timeLeft -=self.sleepInterval
        print('slotShiftState = ',str(self.slotShiftState), '; sleepInterval=',self.sleepInterval)
        if (self.slotShiftState):
            for channel in cfg['active']:
                engine=cfg['engines'][channel]
                try:
                    engine.slots.shiftLeft() #mainly default type classes have a shiftLeft for timeinterval
                except AttributeError:
                    pass
                if self.timeLeft<0:
                    engine.stop=True
        print("Timer woke up!")

def getSlotsJson():
    chartDataArr=[]
    for chNM in cfg['active']:
            chartDataArr.append(cfg['engines'][chNM].getSlotsJson(chNM))
    return json.dumps(chartDataArr)

if __name__ == '__main__':
    #start the threads for websocket read and timer
    rwsArr=[]
    for chNM in cfg['active']:
        rws=readWebsock(chNM,cfg['settings']['noOfMsgs'])
        rwsArr.append(rws)
        rws.start()
    # main thread --> loops and updates the slots and stores them in redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    #Note refresh interval is in milliseconds
    ti=timerForSlotShift(cfg['settings']['slotShiftTimeSecs'],cfg['settings']['refreshInterval'] % 1000,cfg['settings']['totalRunTime'])
    ti.calcTimeState() #set the timestate and sleep interval initially
    print('slotShiftState = ',str(ti.slotShiftState), '; sleepInterval=',ti.sleepInterval
              ,'; slotShiftInterval = ', ti.ns,'; refreshInterval = ',ti.nr)
    while True:
        if ti.timeLeft<0:
            print("Timer stopped!")
            break
        ti.slotShift()
        #Store a json blob in redis
        r.set('chartPanel',getSlotsJson())
        ti.calcTimeState()
        print('slotShiftState = ',str(ti.slotShiftState), '; sleepInterval=',ti.sleepInterval
              ,'; slotShiftInterval = ', ti.ns,'; refreshInterval = ',ti.nr)
        pprint(json.loads(str(r.get('chartPanel'),'utf-8')))
    print("Timer Over -- No more new Data to Redis!")
            
            
            
            
