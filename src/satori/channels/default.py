'''
Created on May 21, 2017

@author: acer
'''
import sys
import threading
import json
from pprint import pprint
import traceback
import re
import unicodedata
import time
import json
from _tracemalloc import stop
from src.cfg import cfg
class slotter:
    def __init__(self,noOfSlots):
        self.noOfSlots=noOfSlots
        self.prevMarker = None
        self.slots =[]
        for i in range(noOfSlots):
            self.slots.append(0)
    def putInslot(self,slotNo,val):
        self.slots[slotNo % self.noOfSlots]=val
    def addRightSlotOld(self,marker,val):
        if self.prevMarker == None:
            self.prevMarker=marker
        #shift slots left (0..noOfSlots-1)
        if self.prevMarker != marker:
            for i in range(self.noOfSlots-1):
                self.slots[i]=self.slots[i+1]
            self.slots[self.noOfSlots-1]=0
            self.prevMarker=marker
    def addToRightSlot(self,val):
        self.slots[self.noOfSlots-1] += val
    def shiftLeft(self):
        #This must be semaphored
        for i in range(self.noOfSlots-1):
            self.slots[i]=self.slots[i+1]
        self.slots[self.noOfSlots-1]=0

    def getSlotsJsonOld(self):
        #Build Json
        #[["Time", "count"], ["0", 5], ["1", 6], ["2", 7]]
        sJson=[]
        sJson.append(["Time", "count"])
        for i in range(self.noOfSlots):
            sj=[]
            sj.append(str(i))
            sj.append(self.slots[i])
            sJson.append(sj)
        return sJson
    def getSlotsJson(self,chNM):
        #Build Json
        #[["Time", "count"], ["0", 5], ["1", 6], ["2", 7]]
        chartJson={}
        chartInfo=cfg['chDetails'][chNM]
        sJson=[]
        sJson.append(["Time", "count"])
        for i in range(self.noOfSlots):
            sj=[]
            sj.append(str(i))
            sj.append(self.slots[i])
            #sj.append("gold")
            sJson.append(sj)
        chartJson['data']=sJson
        return chartJson
    def printSlots(self):
        pprint (self.slots)

class default:
    def __init__(self,maxMsgCount):
        print ('In init of default')
        self.msgCount=0
        self.noOfSlots=5
        self.slots=slotter(self.noOfSlots)
        self.maxMsgCount=maxMsgCount
        self.stop=False
    def stopCondition(self):
        if self.msgCount % 100 ==0:
            print ('msgCount='+str(self.msgCount))
        return self.stop
    def getSlotsJson(self,chNM):
        return self.slots.getSlotsJson(chNM)
    @staticmethod
    def getMsgs(rawData):
        rawData=bytes(rawData,'UTF-8')
        #print (rawData)
        rawData1=rawData.decode("utf-8", "replace")
        rawData1=''.join([a for a in rawData1 if not( unicodedata.category(a) in ['Cc']) ])
        rd=None
        rds=None
        try:
            rds=re.sub('[^\w~!@#$%^&*()_+=\-{}\[\]:"\';<>?/.,\\\\ ]','?',rawData1)
            rd=json.loads(rds)
        except:
            tb=sys.exc_info()[2]
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            traceback.print_tb(tb)
            print (rds)
            print(rawData1)
            sys.exit(1)
        msgs=rd['body']['messages']
        noOfMsgs = len(msgs);
        return noOfMsgs,msgs
    def processMsg(self,rawData):
        noOfMsgs,msgs = default.getMsgs(rawData)
        self.msgCount += noOfMsgs
        self.slots.slots[self.noOfSlots-1] += noOfMsgs

if __name__ == '__main__':
    slots=slotter(5)
        