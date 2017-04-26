# encoding=utf8  
# -*- coding: utf-8 -*-

import numpy as np # used for sparse matrices, could also use for fast binning
import scipy
from scipy import sparse
from scipy import spatial
import pickle
import gzip
from datetime import datetime
import utils.extraFunctions as extraFunctions
import utils.bitOperations as bitOperations
from flask import Flask
from flask import request
import flask
import json
import copy
#import AGOperations
#import KLmatrix



app = Flask("api_flask")
app.config['JSON_AS_ASCII'] = False

print('Flask initiated.')

pathSparse = 'c:/data/sparseBits_batch_apr2017_3'#'c:/data/sparseBits_batch_apr2017_1_small'#'C:/Projects/spark-analysis/Yrken/sparseBits_batch_aug2016_6'#sparseBits_batch_aug2016_7_appended#sparseBits_batch_aug2016_6'#sparseBits_batch_aug2016_1'#sparseBits_sample5'
pathDense = 'c:/data/denseColumns_batch_jan2017_1'#'c:/data/denseColumns_batch_apr2017_1_small'#'C:/Projects/spark-analysis/Yrken/denseColumns_batch_aug2016_6'
#pathAG = 'C:/Projects/spark-analysis/GFR/hashAGSNIs.json'

bitOps = bitOperations.GeneralOperations()
bitOps.LoadData(pathSparse,pathDense)#,pathAG) # will load and convert data into bit arrays
print('Loaded bitops data.')

# cache some data

# AG Operations, not part of HLJ
#AGOps = AGOperations.AGGenerals()
#pathAG = 'C:/Projects/spark-analysis/GFR/'
#AGOps.LoadData(pathAG)

#print 'Loaded AG data.'
# end AG Ops

def calcResult(phrase,getSNI = False):
    #phrase = phrase.lower()
    a = datetime.now()
    bitOps.ReadInput(phrase)

    try:
        bitOps.GetForMonths()
        bitOps.GetForYears()
        #bitOps.GetForOccupations()
        #bitOps.GetForEmployers(getSNI)
        #bitOps.GetForKommuner() # correct (!): this should return zero indexes
    except:
        print('exception retrieving misc.')

    res = bitOps.GetResults()

    b = datetime.now()
    c=b-a
    res['retrieval_time'] = c.total_seconds()

    print('(' + str(c.total_seconds()) + ')')

    return res

def calcKL(phrase,phrase2 = ""):
    a = datetime.now()
    res = bitOps.KLSingle(phrase,phrase2)

    b = datetime.now()
    c=b-a
    res['retrieval_time'] = c.total_seconds()

    print('(' + str(c.total_seconds()) + ')')

    return res

# auto-load ('och')

resOch = copy.deepcopy(calcResult('och'))

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route("/")
def h():
    return "realtime_api1"

@app.route("/realtime1/<path:phrase>")
def trendData(phrase):
    print(phrase)

    # save to file
    with open("inputLog.txt", "a") as myfile:
        myfile.write(str(datetime.now()) + ': ')
        myfile.write(phrase)
        myfile.write('\n')

    if phrase == 'och':
        return flask.jsonify(resOch)#**dataTrend[phrase])
    else:
        res = flask.jsonify(calcResult(phrase))
        return res#**dataTrend[phrase])

@app.route("/realtime2/<path:phrase>/<path:phrase2>")
def KLData(phrase,phrase2):

    print('KL:')
    print(phrase)
    print(phrase2)

    # save to file
    with open("inputKLLog.txt", "a") as myfile:
        myfile.write(str(datetime.now()) + ': ')
        myfile.write(phrase.encode('utf-8'))
        myfile.write(', ')
        myfile.write(phrase2.encode('utf-8'))
        myfile.write('\n')

    return flask.jsonify(calcKL(phrase,phrase2))#**dataTrend[phrase])

# AG Operations, not part of HLJ
@app.route("/realtimeAG/<path:phrase>/<path:ort>")
def AGData(phrase,ort):
    print('AG!')
    print(phrase)
    print(ort)

    res = calcResult(phrase,True)
    #print res
    # calc corresponding AGs

    SNI = res[phrase]['SNI']
    #print SNI

    # get normalized SNIs from 'och'
    normalizedSNIs = resOch['och']['SNI']

    res2 = AGOps.CalcResult(SNI, normalizedSNIs, ort)

    #print res2

    # save to file
    with open("inputLogAG.txt", "a") as myfile:
        myfile.write(str(datetime.now()) + ': ')
        myfile.write(phrase.encode('utf-8'))
        myfile.write('\n')

    return flask.jsonify(res2)#**dataTrend[phrase])

# end AG Operations

@app.route("/realtime2/<path:phrase>")
def KLDataSingle(phrase):
    return KLData(phrase,"")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080, threaded=True)
    #app.run(host='localhost',port=8080)
