#!/usr/bin/env python

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
#from src.satori.channels.bitcoin import bitcoin
class slotter:
    def __init__(self,noOfSlots):
        self.noOfSlots=noOfSlots
        self.prevMarker = None
        self.slots =[]
        for i in range(noOfSlots):
            self.slots.append(0)
    def putInslot(self,slotNo,val):
        self.slots[slotNo % self.noOfSlots]=val
    def addRightSlot(self,marker,val):
        if self.prevMarker == None:
            self.prevMarker=marker
        #shift slots left (0..noOfSlots-1)
        if self.prevMarker != marker:
            for i in range(self.noOfSlots-1):
                self.slots[i]=self.slots[i+1]
            self.slots[self.noOfSlots-1]=0
            self.prevMarker=marker
        self.slots[self.noOfSlots-1] += val
    def getSlotsJson(self):
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
    def printSlots(self):
        pprint (self.slots)
class ch:
    endpoint = "wss://open-data.api.satori.com"
    appkey = "E0Acebca1fbB549AaBeA5D9bec2aacb8"
    urlString = endpoint + '?appkey='+appkey
    chDetails={'bitcoin':{'pDu':{"action":"rtm/subscribe","id":"20","body":{"channel":"bitcoin-transactions"}},'classNM':'bitcoin'},
          'meetup':{'pDu':{"action":"rtm/subscribe","id":"20","body":{"channel":"Meetup-RSVP"}},'classNM':'default'}
          }
    def __init__(self,nM,maxMsgCount):
        self.pDu=ch.chDetails[nM]['pDu']
        self.urlString=ch.endpoint + '?appkey='+ch.appkey
        self.processEngine=globals()[ch.chDetails[nM]['classNM']]
        self.showMessage=self.processEngine.processMsg
        self.stopCondition=self.processEngine.stopCondition
        self.processEngine.maxMsgCount=maxMsgCount
class default:
    msgCount=0
    slots=slotter(5)
    maxMsgCount=-1 #defined externally
    @staticmethod
    def stopCondition():
        print ('msgCount='+str(default.msgCount))
        default.msgCount +=1
        if default.msgCount > default.maxMsgCount:
            return True
        return False
    @staticmethod
    def processMsg(rawData):
        rawData=bytes(rawData,'UTF-8')
        print (rawData)
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
        default.slots.addRightSlot(int(time.clock()/60), noOfMsgs)
        default.msgCount += noOfMsgs

class meetup(default):
    msgCount=0
    @staticmethod
    def stopCondition():
        print ('msgCount='+str(meetup.msgCount))
        meetup.msgCount +=1
        if meetup.msgCount > 1000:
            return True
        return False
    @staticmethod
    def processMsg(rawData):
        rawData=bytes(rawData,'UTF-8')
        print (rawData)
        rawData1=rawData.decode("utf-8", "replace")
        print (type(rawData1))
        rawData1=''.join([a for a in rawData1 if not( unicodedata.category(a) in ['Cc']) ])
        print (type(rawData1))
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
        meetup.msgCount += noOfMsgs
        for msg in msgs:
            if ('group_state' in msg['group']):
                if msg['group']['group_state']=='CA':
                    print(msg['group']['group_city'])
                    try: 
                        print('Got message "{0}"'.format(msg))
                    except:
                        fileNM = 'c:/junk/pprintError.txt'
                        f = open(fileNM,'wb')
                        f.write(rawData1)
                        f.close()
                        sys.exit()

if __name__ == "__main__":
    sr=slotter(5)
    for i in range(10):
            sr.addRightSlot(i, i)
    sr.printSlots()
    pprint(json.dumps(sr.getSlotsJson()))
    sys.exit(0)
    print('Gazebo')
    bt=ch('meetup')
    bt.stopCondition()
    bt.stopCondition()