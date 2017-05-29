'''
Created on May 28, 2017

@author: acer
'''
from flask import Flask,get_template_attribute,send_from_directory
from src.satori.websock import readWebsock
#from src.satori.bitcoin2Old import meetup
from src.satori.channels.ch import ch, timerForSlotShift
import json
import markdown
from pprint import pprint
from src.cfg import cfg
import os
import time
import redis
class timerForSlotShift ():
#at specified time interval shifts slots (should lock slots while shifting..not done yet)
    def __init__(self,intervalSeconds,totalTime):
        super().__init__()
        self.intervalSeconds=intervalSeconds #name of the channel (defined in bitcoin2.ch)
        self.timeLeft=totalTime
    def slotShift(self):
        #urlString = endpoint + '?appkey='+appkey
        time.sleep(self.intervalSeconds)
        self.timeLeft -=self.intervalSeconds
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
    ti=timerForSlotShift(cfg['settings']['slotShiftTimeSecs'],cfg['settings']['totalRunTime'])
    while True:
        if ti.timeLeft<0:
            print("Timer stopped!")
            break
        ti.slotShift()
        #Store a json blob in redis
        r.set('chartPanel',getSlotsJson())
        pprint(json.loads(str(r.get('chartPanel'),'utf-8')))
    print("Timer Over -- No more new Data to Redis!")
            
            
            
            
