__author__ = 'bensm'

import numpy as np # used for sparse matrices, could also use for fast binning
import scipy
from scipy import sparse
from scipy import spatial
import math
import datetime
#import conversions
import extraFunctions

def wordsExists(words,s,doNotSplit,checkSubstring):
    if words == None:
        return [1]
    if s:
        outList = []

        if checkSubstring is True:
            for w in words:
                if w in s:
                    outList.append(1)
                else:
                    outList.append(0)

            return outList

        elif doNotSplit is True: # check entire s only, do not split it up into its parts
            for w in words:
                if w == s:
                    outList.append(1)
                else:
                    outList.append(0)

            return outList
        else:
            #s.encode('utf-8') # no change
            sList = s.lower().split(' ')#s.encode('utf-8').lower().split(' ')

            #outList = map(lambda x: 1 if x in sList else 0, words)
            for w in words:
                if w == s:
                    outList.append(1)
                elif w in sList:
                    outList.append(1)
                else:
                    outList.append(0)

            return outList
    else:
        return [0]*len(words)

def convertToSparseRepr(vec):

    # convert to numpy + transpose shape
    m = np.asarray(vec)
    m = np.transpose(m)

    # return as sparse repr
    mSparse = sparse.csr_matrix(m)

    return mSparse

def getWordVecs(words,allData,type, checkSubstring):
    if type == "PLATSBESKRIVNING":
        wordVecs = allData.select("PLATSBESKRIVNING").map(lambda x: (wordsExists(words,x.PLATSBESKRIVNING, False, checkSubstring)))
        return wordVecs.collect()
    else: # assumed yrkeskategori
        if type == "PUBLICERAD_FROM":
            wordVecs = allData.select("PUBLICERAD_FROM").map(lambda x: (wordsExists(words,x.PUBLICERAD_FROM, True, checkSubstring)))
        elif type == "FORSTA_PUBLICERINGSDATUM":
            wordVecs = allData.select("FORSTA_PUBLICERINGSDATUM").map(lambda x: (wordsExists(words,x.FORSTA_PUBLICERINGSDATUM, True, checkSubstring)))
        elif type == "YRKESBENAMNING" :
            wordVecs = allData.select("YRKESBENAMNING").map(lambda x: (wordsExists(words,x.YRKESBENAMNING, True, checkSubstring)))
        elif type == "YRKE_ID":
            wordVecs = allData.select("YRKE_ID").map(lambda x: (wordsExists(words,x.YRKE_ID, True, checkSubstring)))
        elif type == "KOMMUN_KOD":
            wordVecs = allData.select("KOMMUN_KOD").map(lambda x: (wordsExists(words,x.KOMMUN_KOD, False, checkSubstring)))
        else:
            return []

        return wordVecs.collect()

def getSparseBitVectors(words,wordVecs):

    v = wordVecs
    sparseWordVecs = convertToSparseRepr(v)

    # organize each word
    index = 0;

    dictSparseWordVecs = {}

    # convert to parallelized loop
    for vec in sparseWordVecs:
        if words == None: # Used in calculating total number of everything used in normalization
            w = "_total"
        else:
            w = words[index]
        dictSparseWordVecs[w] = vec

        index=index+1
        if index%50 == 0:
            print index

    return dictSparseWordVecs

def CalcBitVectorsForWords(words,allData,type = "PLATSBESKRIVNING", checkSubstring = False, nrInBatch = 25):

    totSparseBitVectors = {}

    for i in range(0,len(words),nrInBatch):
        iEnd = i+nrInBatch
        if iEnd>len(words):
            iEnd = len(words)

        currentWords = words[i:iEnd]
        for w in currentWords:
            print w
        wordVecs = getWordVecs(currentWords,allData,type, checkSubstring)
        sparseBitVectors = getSparseBitVectors(currentWords,wordVecs)
        totSparseBitVectors.update(sparseBitVectors)
        print 'Current step: ' + str(i) + ' of total ' + str(len(words))

    return totSparseBitVectors;