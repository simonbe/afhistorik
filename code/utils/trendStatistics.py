import math
import pickle
import numpy as np
import scipy
from scipy import sparse
from scipy import spatial

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, 0)#pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def splitText(x):
    if x:
        try:
            return x.lower().split(' ')#x.encode('utf-8').lower().split(' ')#x.encode('utf-8').lower().split(' ')
        except:
            print("Error:")
            print(x)
            return []
        #return x.encode('utf-8').lower().split(' ')
    else:
        return []

def splitTextUniqueWithIndex(x,index):
    if x:
        try:
            listUnique = list(set(x.lower().split(' ')))
            res = [(x,index) for x in listUnique]

            return res
        except:
            print("Error:")
            print(x)
            return []
        #return x.encode('utf-8').lower().split(' ')
    else:
        return []

def splitTextOnMonth(x,index):
    return [(x[0:4] + '-' + x[6:7],index)]

def encodeText(x):
    if x:
        try:
            return x.encode('utf-8').lower()
        except:
            print("Error:")
            print(x)
            return ""
        #return x.encode('utf-8').lower().split(' ')
    else:
        return ""

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def encodeRaw(w):
    w = w.replace('\xc3','xc3')
    w = w.replace('\xa5','xa5')
    w = w.replace('\xb6','xb6')
    w = w.replace('\xa4','xa4')

    return w

def decodeRaw(w):
    w = w.replace('xc3','\xc3')
    w = w.replace('xa5','\xa5')
    w = w.replace('xb6','\xb6')
    w = w.replace('xa4','\xa4')

    return w

def WordInList(word, listWords):
    if not word:
        return True

    if ',' in word:
        return True

    if ':' in word:
        return True

    if word.endswith('.'):
        return True

    if is_number(word):
        return True

    if word in listWords:
        return True
    else:
        return False

def removeLastCharacters(word):
    if word.endswith('.') or word.endswith(',') or word.endswith('?'):
        return word[:-1]
    else:
        return word

def getBigramFreqs(beskr,stopWords):
    if stopWords:
        bigrams = beskr.map(lambda x: splitText(x.PLATSBESKRIVNING)) \
            .flatMap(lambda x: [((x[i],removeLastCharacters(x[i+1])),1) for i in range(0,len(x)-1)]).filter(lambda x: False if (WordInList(x[0][0],stopWords) or WordInList(x[0][1],stopWords)) else True)
    else:
        bigrams = beskr.map(lambda x: splitText(x.PLATSBESKRIVNING)) \
            .flatMap(lambda x: [((x[i],removeLastCharacters(x[i+1])),1) for i in range(0,len(x)-1)])

    freq_bigrams = bigrams.reduceByKey(lambda x,y:x+y) \
        .map(lambda x:(x[1],x[0])) \
        .sortByKey(False)
    return freq_bigrams

def getUnigramFreqs(beskr,stopWords = []):
    if stopWords:
        unigrams = beskr.map(lambda x: splitText(x.PLATSBESKRIVNING)) \
            .flatMap(lambda x: [(removeLastCharacters(x[i]),1) for i in range(0,len(x))])#.filter(lambda x: False if WordInList(x[0],stopWords) else True)
    else:
        unigrams = beskr.map(lambda x: splitText(x.PLATSBESKRIVNING)) \
            .flatMap(lambda x: [(removeLastCharacters(x[i]),1) for i in range(0,len(x))])

    freq_unigrams = unigrams.reduceByKey(lambda x,y:x+y).filter(lambda x: False if WordInList(x[0],stopWords) else True) \
        .map(lambda x:(x[1],x[0])).sortByKey(False)              #decodeRaw(x[0]))) \

    return freq_unigrams

def BuildCSRFromIndices(indices, antalPlatser, maxIndex):
    #maxIndex = max(indices)
    m = np.zeros(len(antalPlatser))#maxIndex+1)
    for i in indices:
        m[i] = antalPlatser[i]

    # return as sparse repr
    mSparse = sparse.csr_matrix(m)

    return mSparse

def GetAllSparseVecs(data,columnName, denseAntalPlatser, doSplitText = False, func = []):

    denseVecs = data.rdd.zipWithIndex()

    if doSplitText == True:
        denseVecs = denseVecs.map(lambda x: splitTextUniqueWithIndex(x[0].asDict()[columnName],x[1])) \
                    .flatMap(lambda x: [(removeLastCharacters(x[i][0]), [ x[i][1] ]) for i in range(0,len(x))])
    else:
        denseVecs = denseVecs.map(lambda x: (x[0].asDict()[columnName],x[1])) \
                    .flatMap(lambda x: [(removeLastCharacters(x[i][0]), [ x[i][1] ]) for i in range(0,len(x))])
    #elif func is not []:
    #    denseVecs = denseVecs.map(lambda x: func(x[0].asDict()[columnName],x[1])) \
    #                .flatMap(lambda x: [(removeLastCharacters(x[i][0]), [ x[i][1] ]) for i in range(0,len(x))])

    # combine lists: ([1,2,3] + [4,5]) becomes [1,2,3,4,5]
    reducedVecs = denseVecs.reduceByKey(lambda x,y:x+y)#.map(lambda x: (x[0],))#.filter(lambda x: True if WordInList(x[0],includedWords) else False)

    tempColl = reducedVecs.filter(lambda x: len(x[1])>20).collect()

    sparseTempColl = {}

    for index in range(0,len(tempColl)):
        item = tempColl[index]
        if(len(item[1])>10):
            spVec = BuildCSRFromIndices(item[1], denseAntalPlatser, max(item[1])+1)
            sparseTempColl[item[0]] = spVec
        tempColl[index] = []

        if index%10000 == 0:
            print(index)
            print(len(sparseTempColl))

    # convert into sparse vectors + collect result
    #reducedVecs = reducedVecs.map(lambda x: (x[0],BuildCSRFromIndices(x[1])))
    #reducedVecs = reducedVecs.collect()

    # convert to dictionary
    #result = {}

    #for item in reducedVecs:
    #    result[item[0]] = item[1]

    return sparseTempColl#result

def KLDivergence(p,q):
    if p==0:
        return 0
    elif q==0:
        return -10000
    else:
        return p*(math.log(p) - math.log(q))

def CalcAndSaveOrderedKL(yrkeA,yrkeRest,yrkeAUni,yrkeRestUni,name):
    dictWeightsUni = {}
    # 1. Unigrams
    for key in yrkeAUni.keys():
        yrkeAVal = yrkeAUni[key]
        yrkeRestVal = 1
        if(key in yrkeRest):
            yrkeRestVal = yrkeRestUni[key]

        informativeness = KLDivergence(yrkeAVal,yrkeRestVal)
        dictWeightsUni[key] = informativeness

    # 2. Bigrams

    #yrkeA = dictTot[yrkeANamn];
    #yrkeRest = dictTot[yrkeRestNamn]
    dictWeights = {}
    for key in yrkeA.keys():
        yrkeAVal = yrkeA[key]
        yrkeRestVal = 1
        if(key in yrkeRest):
            yrkeRestVal = yrkeRest[key]

        words = key.split(' ')
        if words[0] in yrkeAUni and words[1] in yrkeAUni:
            pFirstWord = yrkeAUni[words[0]]
            pSecondWord = yrkeAUni[words[1]]

            phraseness = KLDivergence(yrkeAVal,pFirstWord*pSecondWord)
            informativeness = KLDivergence(yrkeAVal,yrkeRestVal)

            tot = phraseness + informativeness
            dictWeights[key] = tot

    # sort weighted words
    sortedDictUni = {}
    sortedDict = {}

    for w in sorted(dictWeights,key=dictWeights.get,reverse=True):
        sortedDict[w] = dictWeights[w]

    for w in sorted(dictWeightsUni,key=dictWeightsUni.get,reverse=True):
        sortedDictUni[w] = dictWeightsUni[w]

    sortedTuple = sorted(dictWeights.items(), key=lambda x:-x[1])
    sortedTupleUni = sorted(dictWeightsUni.items(), key=lambda x:-x[1])

    with open("KLBigramsCompetences_" + name.replace("/","_") + ".txt", "w") as text_file:
        for item in sortedTuple:
            text_file.write(str(item[0]))
            text_file.write('; ')
            text_file.write(str(item[1]))
            text_file.write('\n')

    with open("KLUnigramsCompetences_" + name.replace("/","_") + ".txt", "w") as text_file:
        for item in sortedTupleUni:
            text_file.write(str(item[0]))
            text_file.write('; ')
            text_file.write(str(item[1]))
            text_file.write('\n')

    save_obj(sortedTupleUni,"unigram_" + name.replace("/","_"))
    save_obj(sortedTuple,"bigram_" + name.replace("/","_"))

    return

def getYrkenCounts(yrkesBenamning):

    mRaw = yrkesBenamning.map(lambda x: (x.YRKESBENAMNING,1))
    countMRaw = mRaw.reduceByKey(lambda x,y:x+y).map(lambda x:(x[1],x[0])).sortByKey(False)

    m = yrkesBenamning.map(lambda x: (encodeText(x.YRKESBENAMNING),1))
    countM = m.reduceByKey(lambda x,y:x+y).map(lambda x:(x[1],x[0])).sortByKey(False)

    # assumes there are no errors in yrkesgrupper_id
    n = yrkesBenamning.map(lambda x: (encodeText(x.YRKESGRUPP_ID),1))
    countN = n.reduceByKey(lambda x,y:x+y).map(lambda x:(x[1],x[0])).sortByKey(False)

    return [countMRaw.collect(), countM.collect(), countN.collect()]

# arbitrary histogram of greatest granularity
def ArbHistogram(allData,subSetData,column):
    # get all possible values from allData
    all = allData.select(column)#.map(lambda x: x)