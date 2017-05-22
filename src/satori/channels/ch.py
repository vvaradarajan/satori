'''
Created on May 21, 2017

@author: acer
'''
from src.satori.channels.bitcoin import bitcoin
from src.satori.channels.default import default
import sys
import inspect
from pprint import pprint
from src.cfg import cfg
class ch:
    endpoint = "wss://open-data.api.satori.com"
    appkey = "E0Acebca1fbB549AaBeA5D9bec2aacb8"
    urlString = endpoint + '?appkey='+appkey
    chClassNamePrefix='src.satori.channels'
#     chDetails={'bitcoin':{'pDu':{
#             "action":"rtm/subscribe","id":"20","body":{"channel":"bitcoin-transactions"}},'classNM':'bitcoin.bitcoin',
#             "charts":{"msgRate":{"Title":"Bitcoin msgs in last 5 mins"}}
#             }
#         ,'meetup':{'pDu':{
#             "action":"rtm/subscribe","id":"20","body":{"channel":"Meetup-RSVP"}},'classNM':'default.default'},
#             "charts":{"msgRate":{"Title":"Meetup msgs in last 5 mins"}}     
#           }
    @staticmethod
    def loadChClassesInCfgObsolete():
        cfg['engines'] = {}
        for chNM in cfg['active']:
            cfg['engines'][chNM]= ch.load_class_from_name(ch.chClassNamePrefix+'.'+cfg['chDetails'][chNM]['classNM'])
        pprint(cfg)
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
        self.urlString=ch.endpoint + '?appkey='+ch.appkey
        processEngineNM=ch.chClassNamePrefix+'.'+cfg['chDetails'][nM]['classNM']
        print('processEngineNM-' + processEngineNM)
        if cfg['chDetails'][nM]['classNM']=='default.default':
            self.processEngine=ch.load_class_from_name(processEngineNM)(maxMsgCount)
        else:
            self.processEngine=ch.load_class_from_name(processEngineNM) #using class - not instance of class
        cfg['engines'][nM]=self.processEngine
        self.showMessage=self.processEngine.processMsg
        self.stopCondition=self.processEngine.stopCondition
        self.processEngine.maxMsgCount=maxMsgCount

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
        