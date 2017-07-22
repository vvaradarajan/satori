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
        print ('In init of defaultLine for '+chNM)
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
        #############Change the self.datasource ############
        consumed = self.otherData.asyncCallList['consumed']['processEngine'].fcnData
        solar = self.otherData.asyncCallList['solar']['processEngine'].fcnData
        tieredPrice = self.otherData.asyncCallList['tieredPrice']['processEngine'].fcnData
        battery = self.otherData.asyncCallList['battery']['processEngine'].fcnData
        if self.valCalc == 'defined':
            return self.chNM,self.getValFromArray(x)
        elif self.chNM == 'netPwrReqd':
            y=consumed[x][1]-solar[x][1]
            self.fcnData[x]=[x,y]
            return self.chNM,y
        elif self.chNM == 'cost':
            y=(consumed[x][1]-(solar[x][1]+battery[x][1]))*tieredPrice[x][1]
            self.fcnData[x]=[x,y]
            return self.chNM,y
        else:
            raise Exception('Invalid chartType: ' + self.chNM)
class summaryDefs():
    def getSummary(self):
        totalCost = sum(y for x,y in self.fcnData)
        print ('Total Cost =',totalCost)
        return totalCost
class cost(defaultLine,summaryDefs):
    def __init__(self,chNM):
        super().__init__(chNM)

class solar(defaultLine,summaryDefs):
    def __init__(self,chNM):
        super().__init__(chNM)
        
class priceTier(defaultLine):
    def __init__(self,chNM):
        super().__init__(chNM)
    def setStateValues(self):
        self.highState = max(self.datasource[self.chNM], key=lambda item: item[1])[1]
        self.lowState = min(self.datasource[self.chNM], key=lambda item: item[1])[1]
    def getState(self,x):
        return 'low' if abs(self.fcnData[x][1] - self.lowState) < 0.001 else 'high'    
class batteryChg(defaultLine):
    def getState(self,chg):
        if chg >=self.ChgMax:
            return 'max'
        elif chg <= self.ChgMin:
            return 'min'
        else:
            return 'norm'
    def __init__(self,chNM):
        super().__init__(chNM)
    def initExplicit(self):  #to be called after creation of all related objects created with properties injected.
        print (self)
        print (self.otherData)
        self.battery = self.otherData.asyncCallList['battery']['processEngine']
        self.fcnData[0] = [0,self.battery.ChgInitial]
        self.state = self.getState(self.battery.ChgInitial)
        print ('In initExplicit of ' + self.chNM)
    async def getResult(self,x):
        #batteryChg is computed for the beginning of the next period
        prevChg=self.fcnData[x][1]
        y = prevChg - self.battery.fcnData[x][1]
        self.state=self.getState(y)
        if (x<23):
            self.fcnData[x+1]=[x+1,y]
        else:
            self.nextState=y #This is tommorrow's beginning charge
        return self.chNM,y
class battery(defaultLine,summaryDefs):
    def __init__(self,chNM):
        super().__init__(chNM)
    def constraintMinMax(self,y,chgVal,chgMin,chgMax,rateState,Pmax,Pmin):
        #ensures that y is constrained so that at the end of the interval(1 hr) the charge is between Min and Max
        yMaxConstraint = min(chgVal - chgMin,Pmax)
        yMinConstraint = max(chgVal - chgMax,Pmin)
        print('y=',y,'; yMaxC=',yMaxConstraint,'; yMinC=',yMinConstraint)
        if y >= yMinConstraint and y<= yMaxConstraint:
            pass
        elif y < yMinConstraint:
            y= yMinConstraint
        else:
            y= yMaxConstraint
        #apply charging rules - charge only when high
        if rateState=='high' and y<0:
            y=0 #do not charge on high
        elif rateState=='low':
            y = 0 if yMinConstraint > 0 else yMinConstraint
        return y
    
    async def getResult(self,x):
        #Note - the otherData property is set in chartGen depending on initParams
        #newPwsReqd if not exceeding PMAX
        #netPwr = self.otherData.asyncCallList['netPwrReqd']['data'][x][1]
        netPwr = self.otherData.asyncCallList['netPwrReqd']['processEngine'].fcnData[x][1]
        rateState =  self.otherData.asyncCallList['tieredPrice']['processEngine'].getState(x)
        print("Battery Charge at : ",x)
        print(self.otherData.asyncCallList['batteryChg']['processEngine'].fcnData)
        batteryChg = self.otherData.asyncCallList['batteryChg']['processEngine']
        chgVal=batteryChg.fcnData[x][1]
        chgMin=batteryChg.ChgMin
        chgMax=batteryChg.ChgMax
        y=netPwr if netPwr<self.Pmax else self.Pmax
        print('batteryChgState',batteryChg.state,'batteryCurrent=',y)
        print("y=",y,";chgVal=",chgVal,"chgMin=",chgMin,"chgMax=",chgMax,"Pmax=",self.Pmax,"Pmin=",self.Pmin)
        y=self.constraintMinMax(y,chgVal,chgMin,chgMax,rateState,self.Pmax,self.Pmin) #Make sure y is within bounds
        print("y=",y)
        self.fcnData[x]=[x,y]
        #pprint(self.fcnData)
        return self.chNM,y

if __name__ == '__main__':
    b=battery('battery')
    #(self,y,chgVal,chgMin,chgMax,rateState,Pmax,Pmin):
    print (b.constraintMinMax(6,30, 4, 30,'high',20,-35))
    pass
        