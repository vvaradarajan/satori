'''
Created on May 28, 2017

@author: Vasan
@note: This is the main program that generates data for a chart array:
Overview:
f(x)
For each chart f(x) is implemented elsewhere (the class is dynamically imported from the chart array).
The process:
1. Reads Chart Array details from cfg
2. Dynamically create the generator object into an array:
    [cfgObject (containing chart-class), x-value, y-returned]
3. Loop over array:
    increment x-value
    get async loop
    add the async chart-class call (use asyncio.ensure_future). Pass the x-value to each. They read the x-value return the y-value
    wait till all tasks complete and gather the y-values
    update redis with the values
3. Design of the chart-class:
These must implement async getChartData(x) function (Currently subclass is not used as it is the only function)
'''
import json
from pprint import pprint
from src.cfg_power import cfg_power as cfg
import time
import asyncio
import logging
import os
from pprint import pprint
from src.satori.utils import load_class_from_name
from src.satori.utils import transformArrayToScale
import redis
class chart:
    #init create an dict with channelNames [[asyncClassNM,x
    def __init__(self,cfg):
        self.asyncCallList={}
        self.classPrefix = 'src.satori.batteryChannels.'
        self.chartGroups = cfg['chartGroupings']
        asyncLevels={}
        for ch in cfg['active']:
            self.asyncCallList[ch]={}
            #put in callListOrder (async procs will be called by the levels - assume that active list is consistent (i.e. required levels are there)
            asyncLevel = str(0 if not ('asyncLevel' in cfg['chDetails'][ch]) else cfg['chDetails'][ch]['asyncLevel'])
            if not (asyncLevel in asyncLevels.keys()):
                asyncLevels[asyncLevel] = [ch]
            else:
                asyncLevels[asyncLevel].append(ch)
            #collect the classes for each channel
            self.asyncCallList[ch]['classNM']=cfg['chDetails'][ch]['classNM']
            self.asyncCallList[ch]['processEngine']= load_class_from_name(self.classPrefix 
                                                        + self.asyncCallList[ch]['classNM'])(ch)
            #set properties of object
            if 'properties' in cfg['chDetails'][ch]:
                for key,value in cfg['chDetails'][ch]['properties'].items():
                    setattr(self.asyncCallList[ch]['processEngine'],key,value)
        self.asyncLevels=asyncLevels
        pprint("asyncLevels:")
        pprint(asyncLevels)    
        self.processDynamicDataFromFile()
        self.storeSettingsInRedis() #settings for the webserver
    
    def storeSettingsInRedis(self):
        js=cfg['settings']
        print(self.asyncCallList.keys())
        singleList = list(filter(self.isInGroup, self.asyncCallList.keys())) #clone the active
        pprint(singleList)
        #js['noOfPanelCharts']=len(cfg['active'])
        js['noOfPanelCharts']=len(singleList) + len(self.chartGroups)
        chartMixins=[]
        #for c in cfg['active']:
        for c in singleList:
            mixin=cfg['chDetails'][c]['charts']['msgRate']['mixin']
            mixin['id']=c
            chartMixins.append(mixin)
        for group in self.chartGroups:
            mixin=group['mixin']
            mixin['id']=group['id']
            chartMixins.append(mixin)     
        js['chartMixins']=chartMixins
        redisMem.set('settings',json.dumps(js))
        return

    def processDynamicDataFromFile(self):
        dataFileNM  = os.path.join(os.path.dirname(__file__),'satori/batteryChannels/Data/power.txt') #<-- absolute dir the script is in
        #process data points
        newData={}
        with open(dataFileNM) as f:
            fileContent = eval(f.read())
            #print (newData)
        for chNM in fileContent.keys():
            if 'data' in fileContent[chNM]:
                newData[chNM]= transformArrayToScale(fileContent[chNM]['data'])
        self.datasource=newData
        for chNM in self.asyncCallList.keys():
            self.asyncCallList[chNM]['processEngine'].setDatasource(self.datasource)
        #process properties
        for chNM in fileContent.keys():
            if 'properties' in fileContent[chNM]:
                for key,value in fileContent[chNM]['properties'].items():
                    if key=='otherData':
                        setattr(self.asyncCallList[chNM]['processEngine'],key,self)
                    else:
                        setattr(self.asyncCallList[chNM]['processEngine'],key,value)
            #set the tier values for tieredPrice
            if 'tier' in chNM:
                self.asyncCallList[chNM]['processEngine'].setStateValues()

    def addToAsyncLoop(self,chList,loop,x):
        for ch in chList:
            print (ch,str(x))
            asyncio.ensure_future(self.asyncCallList[ch]['processEngine'].getResult(x))  #add task to current loop 

    def generateChartData(self):
        #generate data by async level (level indicates that all async's lower should finish before higher levels can be called)
        for chNM in self.asyncCallList.keys():
            self.asyncCallList[chNM]['data']=[] #clear out old data (#graph data will be put here as an array of x,y points)
        for level in sorted(self.asyncLevels):
            chnlsByLevel=self.asyncLevels[level]
            pprint(chnlsByLevel)
            for i in range(24):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop) # <----
                self.addToAsyncLoop(chnlsByLevel,loop,i)
                pending = asyncio.Task.all_tasks()
                Results = loop.run_until_complete(asyncio.gather(*pending))
                loop.close()
        for chNM in self.asyncCallList.keys():
            pprint(chNM)
            pprint(self.asyncCallList[chNM]['processEngine'].fcnData)
        allChartData = self.getSlotsJson()
        print('allChartData : ')
        pprint(allChartData)
        #put into redis
        redisMem.set('chartPanel',json.dumps(allChartData))
    
    def isInGroup(self,chNM):
            for groups in self.chartGroups:
                if chNM in groups['charts']:
                    return False
            return True

    def getSlotsJson(self):
        retValArr=[] #Array of chartDataObjects - each object has key of chart and an object describing the data
        #create sets of grouped charts
        #first create the non-grouped charts

        singleList = list(filter(self.isInGroup, self.asyncCallList.keys())) #clone the active
        
        for chNM in singleList: #self.asyncCallList.keys():
            retVal={}
            retVal[chNM]={}
            retVal[chNM]['data']=[]
            retVal[chNM]['data'].append(['Time','Value'])
            #retVal[chNM]['data'].extend(self.asyncCallList[chNM]['data'])
            retVal[chNM]['data'].extend(self.asyncCallList[chNM]['processEngine'].fcnData)
            retValArr.append(retVal)
        #The groups have a column for each member of the group
        print (self.chartGroups,len(self.chartGroups))
        for group in self.chartGroups:
            groupId = group['id']
            cols=['Time']
            cols.extend([chNM for chNM in group['charts']])
            print(groupId,': cols = ',cols,'length=',len(group['charts']))
            retVal={}
            retVal[groupId]={}
            retVal[groupId]['data']=[cols]
            dataTbl = [[x[0]] for x in self.asyncCallList[group['charts'][0]]['processEngine'].fcnData]
            for i in range(len(dataTbl)):
                for chNM in group['charts']:
                    dataTbl[i].append((self.asyncCallList[chNM]['processEngine'].fcnData)[i][1])
            retVal[groupId]['data'].extend(dataTbl)
            retValArr.append(retVal) 
        return retValArr
            
if __name__ == '__main__':
    redisMem = redis.Redis(host='localhost', port=6379, db=0)
    logfileNM = '/tmp/chToRedis.log' if (os.name != 'nt') else 'c:/junk/chToRedis.log'
    logging.basicConfig(filename=logfileNM, level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger(__name__)
    log.info("Starting chartGen")
    chnls = chart(cfg)
    #loop = asyncio.get_event_loop()
    noOfCharts = len(cfg['chDetails'])
    print('No of Charts= '+str(noOfCharts))
    chnls.generateChartData()
    #Loop checking if reload is requested
    while True:
        time.sleep(2)
        #check if load file has been specified
        reloadFlag = redisMem.get('reloadData').decode('utf-8')
        if reloadFlag == 'T':
            redisMem.set('reloadData','F')
            chnls.setDatasource()
            chnls.generateChartData()
    
