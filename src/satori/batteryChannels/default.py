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
from src.runMe import cfg
import os
import asyncio

class defaultLine:
    def __init__(self,chNM):
        print ('In init of defaultLine')
        self.chNM = chNM
        
    def setDatasource(self,ds):
        self.datasource = ds 
        if self.valCalc == 'defined':
            self.fcnData = self.datasource[self.chNM]
        else:
            #create an empty array of 24 elements
            self.fcnData = [0 for i in range(24)]        
    def getValFromArray(self,x):
        for i in range(24):
            if x==self.fcnData[i][0]:
                y=self.fcnData[i][1]
        return y
    
    async def getResult(self,x):
        consumed = self.datasource['consumed']
        solar = self.datasource['solar']
        tieredPrice = self.datasource['tieredPrice']
        if self.valCalc == 'defined':
            return self.chNM,self.getValFromArray(x)
        elif self.chNM == 'netPwrReqd':
            y=[x[1]-y[1] for x,y in zip(consumed,solar)][x]
            self.fcnData[x]=[x,y]
            return self.chNM,y
        elif self.chNM == 'cost':
            y=[(a[1]-b[1])*c[1] for a,b,c in zip(consumed,solar,tieredPrice)][x]
            self.fcnData[x]=[x,y]
            return self.chNM,y
        else:
            raise Exception('Invalid chartType: ' + self.chNM)
class priceTier(defaultLine):
    def __init__(self,chNM):
        super().__init__(chNM)
        print ('In init of priceTier')
    def setStateValues(self):
        self.highState = max(self.datasource[self.chNM], key=lambda item: item[1])[1]
        self.lowState = min(self.datasource[self.chNM], key=lambda item: item[1])[1]
    def getState(self,x):
        pprint(self.lowState)
        pprint(self.fcnData[x][1])
        return 'low' if abs(self.fcnData[x][1] - self.lowState) < 0.001 else 'high'    
class battery(defaultLine):
    def __init__(self,chNM):
        super().__init__(chNM)
        print ('In init of battery')
    async def getResult(self,x):
        #Note - the otherData property is set in chartGen depending on initParams
        #newPwsReqd if not exceeding PMAX
        #netPwr = self.otherData.asyncCallList['netPwrReqd']['data'][x][1]
        netPwr = self.otherData.asyncCallList['netPwrReqd']['processEngine'].fcnData[x][1]
        rateState =  self.otherData.asyncCallList['tieredPrice']['processEngine'].getState(x)
        if rateState == 'low':
            y=self.Pmin
        else:
            y=netPwr if netPwr<self.Pmax else self.Pmax
        self.fcnData[x]=[x,y]
        return self.chNM,y

if __name__ == '__main__':
    pass
        