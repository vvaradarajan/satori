from flask import Flask,get_template_attribute,send_from_directory
from src.satori.websock import readWebsock
#from src.satori.bitcoin2Old import meetup
from src.satori.channels.ch import ch
import json
from pprint import pprint
from src.cfg import cfg
app = Flask(__name__,static_url_path='/static')
 
@app.route("/a")
def hello():
    return "Hello World!"

@app.route("/template") 
def helloTpt():
    hello = get_template_attribute('hellotemplate.txt', 'hello')
    return hello('World')

@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory('../bower_components', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('../images', path)

@app.route('/settings/<path:setting>')
def send_settingsData(setting):
    if setting=='all':
        js=cfg['settings']
        js['noOfPanelCharts']=len(cfg['active'])
        return json.dumps(js)
        
    if setting == 'noOfPanelCharts':
        return str(len(cfg['active']))
    return "0"

@app.route('/satori/<path:menuItem>')
def send_satori(menuItem):
    if menuItem=='Chart':
        chNM=cfg['active'][0]
        chartClass=cfg['engines'][chNM]
        pprint(chartClass.slots.getSlotsJson(chNM))
        return json.dumps(chartClass.slots.getSlotsJson(chNM))
    print('menuItem is: '+menuItem)
    if menuItem=='ChartPanel':
        chartDataArr=[]
        pprint(cfg['engines'])
        for chNM in cfg['active']:
            chartDataArr.append(cfg['engines'][chNM].slots.getSlotsJson(chNM))
        return json.dumps(chartDataArr)
            
        #return '[["Time", "count"], ["0", 5], ["1", 6], ["2", 7]]'
    msg='Did you get it from satori: {0}'.format(menuItem)
    return "{'Message':'"+msg+"'}"


if __name__ == "__main__":
    #ch.loadChClassesInCfg()
    rwsArr=[]
    for chNM in cfg['active']:
        rws=readWebsock(chNM,100)
        rwsArr.append(rws)
        rws.start()
    app.run()