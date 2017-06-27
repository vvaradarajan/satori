'''
Created on May 21, 2017

@author: acer
'''
from src.satori.channels.bitcoin import bitcoin
from src.satori.channels.default import default
import sys
import inspect
from pprint import pprint
from src.runMe import cfg
from asyncio.tasks import sleep
class ch:
    chClassNamePrefix='src.satori.channels' #location of channel processing classes
#cfg.py contains the central data structure from which websocket details are loaded

    @staticmethod
    def load_class_from_name(fqcn):
        # Break apart fqcn to get module and classname
        paths = fqcn.split('.')
        modulename = '.'.join(paths[:-1])
        classname = paths[-1]
        # Import the module
        __import__(modulename, globals(), locals(), ['*'])
        # Get the class
        cls = getattr(sys.modules[modulename], classname)
        # Check cls
        if not inspect.isclass(cls):
           raise TypeError("%s is not a class" % fqcn)
        # Return class
        return cls

    def __init__(self,nM,maxMsgCount):
        self.pDu=cfg['chDetails'][nM]['pDu']
        self.urlString=cfg['websocketDetails']['endpoint'] + '?appkey='+cfg['websocketDetails']['appkey']
        processEngineNM=ch.chClassNamePrefix+'.'+cfg['chDetails'][nM]['classNM']
        print('processEngineNM-' + processEngineNM)
        self.processEngine=ch.load_class_from_name(processEngineNM)(maxMsgCount)
        cfg['engines'][nM]=self.processEngine
        self.showMessage=self.processEngine.processMsg
        self.stopCondition=self.processEngine.stopCondition

import threading
import time
class timerForSlotShift (threading.Thread):
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
    def run(self):
        while True:
            if self.timeLeft<0:
                print("Timer stopped!")
                break
            self.slotShift()

if __name__ == "__main__":
    ch.loadChClassesInCfg()
    print('Hello')
    pprint ( cfg)
    for chNM in cfg['active']:
        myCh=ch(chNM,1000)
        chartClass=cfg['engines'][chNM]
        chartClass.slots.addRightSlot(1, 100)
        print(chartClass.maxMsgCount)
        pprint(chartClass.slots.getSlotsJson())
        