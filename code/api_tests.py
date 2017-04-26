# -*- coding: utf-8 -*-
import numpy as np # used for sparse matrices, could also use for fast binning
import scipy
from scipy import sparse
from scipy import spatial
import pickle
import cPickle
import gzip
from datetime import datetime
import extraFunctions
import bitOperations

def load_obj(name ):
    with gzip.open(name + '.pklz', 'rb') as f:
        return cPickle.load(f)

def XORBitSum(vec1,vec2):
    return vec1.dot(vec2.transpose()).sum();

def SparseBitVectorXOR(vec1,listVec):

    result = [0]*len(listVec)
    for i in range(len(listVec)):
        result[i] = XORBitSum(vec1,listVec[i])

    return result

def TestSparseBitVectorXOR(vec1,vec2):

    return []

def GetData(words,dict):

    result = []
    for w in words:
        result.append(dict[w])

    return result

# test Bit operations class
bitOps = bitOperations.GeneralOperations()

pathSparse = 'c:/Data/sparseBits_batch_jan2017_1'
pathDense = 'c:/Data/denseColumns_batch_jan2017_1'
pathAG = 'C:/Projects/spark-analysis/GFR/hashAGSNIs.json'

bitOps.LoadData(pathSparse,pathDense,pathAG)#'sparseBits_batch_aug2016_mini','denseColumns_batch_aug2016_mini','C:/Projects/spark-analysis/GFR/hashAGSNIs.json')#'sparseBits_sample5')

def calcResult(phrase,getSNI = True):
    a = datetime.now()
    bitOps.ReadInput(phrase)
    bitOps.GetForMonths()

    try:
        bitOps.GetForYears()
        bitOps.GetForOccupations()
        bitOps.GetForEmployers(getSNI)
        bitOps.GetForKommuner() # correct (!): this should return zero indexes
    except:
        print 'exception retrieving misc.'

    res = bitOps.GetResults()

    b = datetime.now()
    c=b-a
    res['retrieval_time'] = c.total_seconds()

    print '(' + str(c.total_seconds()) + ')'

    return res


a = datetime.now()

res = calcResult('java')

b = datetime.now()
c=b-a

# get the corresponding best matches given the SNI codes in e.g. 'Sundbyberg'
sniRes = res['java']['SNI']

# weight codes
#AGOps = AGOperations.AGGenerals()
#pathAG = 'C:/Projects/spark-analysis/GFR/'
#AGOps.LoadData(pathAG)

#normalizedSNIs = calcResult('och')['och']['SNI']
#res = AGOps.CalcResult(sniRes,normalizedSNIs,'Gotland')

#weightedRes = []
#for i in range(len(sniRes['Counts'])):
#    sniRes

print res

for r in res:
    print r[0]
    print r[2]['namn']
    print r[2]['naringsgren']
    print '\n'

print c.total_seconds()


print 'end'

# Exempel:
# 1. hur många av programmeringsannonserna efterfrågade javascript; javascript Systemutveckling,Systemutveckling
# 2. hur många efterfrågade flexibel och ansvarsfull: (flexibel ansvarsfull)
# 3. i vilka yrken efterfrågas mjuka kompetenser? kreativ;...
# 4. vilka utbildningar krävs inom Systemutvecklare? (högskoleexamen master mastersexamen) Systemutvecklare,(phd doktorsexamen) Systemutvecklare, Systemutvecklare
# 5. vilket yrke borde jag söka mig till (naive bayes)? '(jag tycker om att spela golf och mecka med maskiner och bilar)'
# 6. .net eller java i olika delar av landet?