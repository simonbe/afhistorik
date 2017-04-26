# encoding=utf8
__author__ = 'bensm'

import os
import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
import csv
import numpy as np # used for sparse matrices, could also use for fast binning
import scipy
from scipy import sparse
from scipy import spatial
import math
import datetime
#import conversions
import extraFunctions
import trendStatistics
import trendBitVectors
import cPickle as pickle
import gzip
import json

reload(sys)
sys.setdefaultencoding('utf8')

doSparseCalc = True
loadSparseUnigrams = False

#doYears = True
#doMonths = True
#doRegions = True

doDenseCalc = True

filenameSaveSparse = 'sparseBits_batch_apr2017_1_small'
filenameSaveDense = 'denseColumns_batch_apr2017_1_small'

with open('yrkeIdNamn.json', 'r') as fp:
    _yrkeIdName = json.load(fp)

with open('kommunKodNamn.json', 'r') as fp:
    _kommunKodNamn = json.load(fp)

path = "C:/Data/platsbanken_anonymized_NEW/*.json"

def save_obj(obj, name ):
    with gzip.open(name + '.pklz', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    data = []
    with gzip.open(name+ '.pklz', 'rb') as f:
         data = pickle.load(f)
    return data

# Initialize SparkContext

SparkContext.setSystemProperty('spark.default.parallelism','50')
SparkContext.setSystemProperty('spark.executor.memory', '3g') # memory for each node
SparkContext.setSystemProperty('spark.executor.cores', '2')
SparkContext.setSystemProperty('spark.driver.cores','2')
SparkContext.setSystemProperty('spark.driver.memory','14g')
SparkContext.setSystemProperty('spark.python.worker.memory','4g')
SparkContext.setSystemProperty('spark.sql.shuffle.partitions','80')
SparkContext.setSystemProperty("spark.driver.maxResultSize", "12g")

sc = SparkContext('local[7]', 'Ex1')
sqlContext = SQLContext(sc)

# get all data
allData = sqlContext.read.json(path)
allData = allData.sample(False,0.05,None)
allData = allData.coalesce(14)#91)


nameYrken = "YRKE_ID"
namePublished = "FORSTA_PUBLICERINGSDATUM"
nameKommun = "KOMMUN_KOD"
nameBeskrivning = "PLATSBESKRIVNING"

#allYrkeData = extraFunctions.GetYrkeData(allData, '', nameYrken)
#topNrs = 500#7500
#startUniIndex = 0


# make and save all concepts/words into sparse bit vectors for real-time histograms

if doSparseCalc == True:
    sparseBitVectors = {}

    # get antal platser as dense vector
    denseAntalPlatser = allData.select("ANTAL_AKT_PLATSER").flatMap(lambda x: x).collect()
    for i in range(0,len(denseAntalPlatser)):
        denseAntalPlatser[i] = int(denseAntalPlatser[i])

    # 1a. get for all unigrams
    print 'Do for unigrams'

    if loadSparseUnigrams == True:
        print 'Loading unigram data.'
        sparseBitVectors = load_obj('sparseBits_batch_jan2017_1_onlyWords')
    else:
        res = trendStatistics.GetAllSparseVecs(allData,"PLATSBESKRIVNING", denseAntalPlatser, True)
        sparseBitVectors.update(res)
        save_obj(sparseBitVectors,'sparseBits_batch_jan2017_1_onlyWords')

    # 1b. get all yrken
    print 'Do for all occupations'
    #yrkesBenamningar = extraFunctions.GetAllOccupations()
    yrkesIds = _yrkeIdName.keys()
    #yrkeVecs = trendBitVectors.CalcBitVectorsForWords(yrkesIds, allData, nameYrken, False, 14)
    #sparseBitVectors.update(yrkeVecs)
    #sparseBitVectors.update(trendBitVectors.CalcBitVectorsForWords(yrkesIds[0:1000], allData, nameYrken, False, 14))
    #sparseBitVectors.update(trendBitVectors.CalcBitVectorsForWords(yrkesIds[1000:2000], allData, nameYrken, False, 14))
    #sparseBitVectors.update(trendBitVectors.CalcBitVectorsForWords(yrkesIds[2000:3000], allData, nameYrken, False, 14))
    #sparseBitVectors.update(trendBitVectors.CalcBitVectorsForWords(yrkesIds[3000:], allData, nameYrken, False, 14))

    yrkeVecs = trendStatistics.GetAllSparseVecs(allData,"YRKE_ID", denseAntalPlatser, True)
    sparseBitVectors.update(yrkeVecs)

    # also copy these (if possible) into their corresponding names -
    # !! case sensitive
    yrkeNames = {}
    for key in yrkeVecs.keys():
        if key in _yrkeIdName.keys():
            yrkeNames[_yrkeIdName[key]] = yrkeVecs[key]

    sparseBitVectors.update(yrkeNames)


    #ANTAL_AKT_PLATSER

    # 1c. get all months
    print 'Do for all months'
    months = extraFunctions.GetAllMonths()
    monthVecs = trendBitVectors.CalcBitVectorsForWords(months, allData, namePublished, True, 50)
    sparseBitVectors.update(monthVecs)
    #res = trendStatistics.GetAllSparseVecs(allData,"FORSTA_PUBLICERINGSDATUM", False, trendStatistics.splitTextOnMonth)
    #sparseBitVectors.update(res)

    # 1d. get all years
    print 'Do for all years'
    years = extraFunctions.GetAllYears()
    yearVecs = trendBitVectors.CalcBitVectorsForWords(years, allData, namePublished, True, 50)
    sparseBitVectors.update(yearVecs)

    # 1e. get all kommuner
    print 'Do for all regions'
    kommuner = extraFunctions.GetAllKommunKoder()
    kommunVecs = trendBitVectors.CalcBitVectorsForWords(kommuner, allData, nameKommun, False, 50)

    sparseBitVectors.update(kommunVecs)

    # 2. Save bit vectors
    print 'Save bit vectors of size '
    print len(sparseBitVectors)

    save_obj(sparseBitVectors,filenameSaveSparse)

    sparseBitVectors.clear()

if doDenseCalc == True:
    # 3. Also save specific columns separately as compressed dense vectors
    print 'Generate dense vectors'
    arbetsgivare = allData.select("AG_NAMN").flatMap(lambda x: x).collect()
    yrke_id = allData.select("YRKE_ID").flatMap(lambda x: x).collect()
    denseDict = {}
    denseDict['arbetsgivare'] = arbetsgivare
    denseDict['yrke_id'] = yrke_id

    print 'Save dense vectors'
    save_obj(denseDict,filenameSaveDense)

print 'Ok, all done.'