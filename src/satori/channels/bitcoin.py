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
from pprint import pprint
class bitcoin(default):
    chNM='bitcoin'
    msgCount=0
    slots=slotter(5)
    maxMsgCount=-1 #defined externally
    @staticmethod
    def stopCondition():
        print ('msgCount='+str(bitcoin.msgCount))
        if bitcoin.msgCount > bitcoin.maxMsgCount:
            return True
        return False
    @staticmethod
    def processMsg(rawData):
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
        bitcoin.msgCount += noOfMsgs
        bitcoin.slots.addRightSlot(int(time.clock()/60), noOfMsgs)
        pprint(bitcoin.slots)
        for msg in msgs:
            if (msg['x']['out']):
              for t in msg['x']['out']:
                value=t['value']

if __name__ == "__main__":
    pass