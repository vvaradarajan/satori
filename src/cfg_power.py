'''
Created on May 21, 2017

@author: acer
'''
cfg_power={'showCharts':['solar','consumed','batteryChg','battery']
           #['solar','consumed','netPwrReqd','tieredPrice','cost','battery','batteryChg'] 
           #['exchange','Flying-A320s','meetup','github','bitcoin','Bart','twitter'] #
     ,'xAxisIntervalInMins':60 #implemented only hourly now
     ,'chartGroupings':[
         {"id":"pwrSolCon","mixin":{"Title":"Solar,Consumed","colors": ['black', 'red','green'],"chartType":'line',"haxis_title":"Hour 0-23"}
           ,"charts":['solar','consumed','battery','cost','batteryChg','tieredPrice']}
         ] #These charts will be in one
     ,'settings':{'refreshInterval':60000,'noOfMsgs':10000,'slotShiftTimeSecs':10,'totalRunTime':72000
                  ,'main-title':'Satori Channel traffic rates..'
                  ,'menuitems':['ReloadData','Chart','ChartPanel','Algorithm','Blog','About']
                  ,'defaultMenuItem':'ChartPanel'}
     ,'chDetails': {
        'solar':{'classNM':'default.solar','properties':{'valCalc':'defined'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Solar Power Output","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'consumed':{'classNM':'default.defaultLine','properties':{'valCalc':'defined'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Power Consumption","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'netPwrReqd':{'classNM':'default.defaultLine','asyncLevel':2,'properties':{'valCalc':'calculated'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Net Power Required","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'tieredPrice':{'classNM':'default.priceTier','properties':{'valCalc':'defined'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Tiered Price/kwH","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'cost':{'classNM':'default.cost','asyncLevel':5,'properties':{'valCalc':'calculated'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"cost each hr","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'battery':{'classNM':'default.battery','asyncLevel':3,'properties':{'valCalc':'calculated'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Power from Battery","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
        ,'batteryChg':{'classNM':'default.batteryChg','asyncLevel':4,'properties':{'valCalc':'calculated'},
                "charts":{"msgRate":{
                    "mixin":{"Title":"Battery Charge","chartType":'line',"haxis_title":"Hour 0-23"}}}
         }
    }
     ,'engines':{} #placeholder to store the processing engines (created from classNM) during run
}
if __name__ == '__main__':
    pass