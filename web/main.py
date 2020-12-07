from flask import Flask
from flask import render_template
from flask import request

import os
import json
from string import Template 

# switch current working path to the location of main.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if ("AZUREFILE" in os.environ and os.environ['AZUREFILE']):
    app = Flask(__name__, static_url_path="/", static_folder= os.environ['AZUREFILE'] + "/static")
    dynamicPath = os.environ['AZUREFILE'] + "/dynamic"
    print("Running env is on Azure")
else:
    app = Flask(__name__, static_url_path="", static_folder= os.getcwd()+"/static")
    dynamicPath = os.getcwd() + "/dynamic"

if ("LOCATION" in os.environ and os.environ['LOCATION']):
    location = os.environ['LOCATION']
else:
    location = "KangXH"

@app.route('/')
@app.route('/index')
def index():
    with open(dynamicPath + '/index.json', 'r') as indexJson:
        indexStream = indexJson.read()

    indexConfig = json.loads(indexStream)
    return render_template('index.html', title='kangxh@Azure', name = location, apps = indexConfig["apps"], projects = indexConfig["projects"], gitrepos = indexConfig["gitrepos"])

@app.route('/identity')
@app.route('/iaas')
@app.route('/container')
@app.route('/microservice')
@app.route('/app')
@app.route('/iot')
@app.route('/contact')
def details():
    urlPath = request.full_path.strip('/').strip('?')

    if urlPath == "contact": 
        return render_template('details.html', service = False)
    else:
        configFile = Template(dynamicPath + '/$details.json')
        urlPath = request.full_path.strip('/').strip('?')
        configFile = configFile.substitute(details = urlPath)

        with open(configFile, 'r') as configJson:
            configStream = configJson.read()
        configJson = json.loads(configStream)
        return render_template('details.html', service = True, scenarios = configJson["scenarios"])

if __name__ == '__main__':
    app.run()