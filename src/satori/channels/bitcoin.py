'''
Created on May 21, 2017

@author: acer
'''
from src.satori.channels.default import default,slotter

import json
import re
import unicodedata
import sys
import traceback
import time
from src.cfg import cfg
from pprint import pprint
class bitcoin(default):
    def __init__(self,noOfSlots):
        super(bitcoin, self).__init__(noOfSlots)
        print ("inited bitcoin")
        self.chNM='bitcoin'

    def processMsg(self,rawData):
        noOfMsgs,msgs = self.getMsgs(rawData)
        pprint(msgs[0])
        self.msgCount += noOfMsgs
        self.slots.slots[self.noOfSlots-1] += noOfMsgs
        
    def processMsgNew(self,rawData):
        rawData=bytes(rawData,'UTF-8')
        print (rawData)
        rawData1=rawData.decode("utf-8", "replace")
        #print (type(rawData1))
        rawData1=''.join([a for a in rawData1 if not( unicodedata.category(a) in ['Cc']) ])
        #print (type(rawData1))
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
        print('noOfMsgs = ' + str(noOfMsgs))
        self.msgCount += noOfMsgs
        self.slots.addRightSlot(int(time.clock()/60), noOfMsgs)
        pprint(bitcoin.slots)
        for msg in msgs:
            if (msg['x']['out']):
              for t in msg['x']['out']:
                value=t['value']

class exchange():
    def __init__(self,maxMsgCount):
        currArray={}
        self.currencies=['AUD','EUR','INR','JPY','CNY']
        self.noOfSlots=len(self.currencies)
        self.slots=[0 for i in range(self.noOfSlots)]
        self.msgCount=0
        self.stop=False

    def processMsg(self,rawData):
        noOfMsgs,msgs = default.getMsgs(rawData)
        pprint(msgs[0])
        self.msgCount += noOfMsgs
        msg=msgs[0] #only one msg
        for idx,sym in enumerate(self.currencies):
            if sym in msg['rates'].keys():
                self.slots[idx]=msg['rates'][sym]
    
    def getSlotsJson(self,chNM):
        chartJson={}
        chartInfo=cfg['chDetails'][chNM]
        chartJson['title']=chartInfo['charts']['msgRate']['Title']
        sJson=[]
        sJson.append(["Time", "count"])
        for i in range(self.noOfSlots):
            sj=[]
            sj.append(self.currencies[i])
            sj.append(self.slots[i])
            #sj.append("gold")
            sJson.append(sj)
        chartJson['data']=sJson
        return chartJson    
    def stopCondition(self):
        if self.msgCount % 100 ==0:
            print ('msgCount='+str(self.msgCount))
        return self.stop #self.stop is set by the timer
    def processMsgNew(self,rawData):
        rawData=bytes(rawData,'UTF-8')
        print (rawData)
        rawData1=rawData.decode("utf-8", "replace")
        #print (type(rawData1))
        rawData1=''.join([a for a in rawData1 if not( unicodedata.category(a) in ['Cc']) ])
        #print (type(rawData1))
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
        print('noOfMsgs = ' + str(noOfMsgs))
        self.msgCount += noOfMsgs
        self.slots.addRightSlot(int(time.clock()/60), noOfMsgs)
        pprint(bitcoin.slots)
        for msg in msgs:
            if (msg['x']['out']):
              for t in msg['x']['out']:
                value=t['value']
if __name__ == "__main__":
    pass