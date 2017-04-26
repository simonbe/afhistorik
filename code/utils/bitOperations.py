# -*- coding: utf-8 -*-

# Bit operations + basic interpreter for text input
# Interpreter:
# '(...)': combine/OR/UNION
# ',' : treat independently
# ' ': AND

# Example: 'javascript html' -> Must include both
# '(javascript html)' -> include javascript or html
# 'javascript,html' -> return both javascript and html

import numpy as np # used for sparse matrices, could also use for fast binning
import scipy
from scipy import sparse
from scipy import spatial
import pickle
#import cPickle
import gzip
from datetime import datetime
import utils.extraFunctions as extraFunctions
#import bitarray
import collections
import json

class BitOperations:

    def BitUnion(self,vec1,vec2): # OR
        return vec1.maximum(vec2)

    def BitAND(self,vec1,vec2): # AND
        return vec1.minimum(vec2)
        # alternatives:
        #a = vec2.multiply(vec1)
        #for i in range(0,10,1):
        #    b = vec2.multiply(vec1)
        #return vec1.multiply(vec2)#vec1.multiply(vec2) # not fast since these are bits, int(vec1-vec2>0) must be better

    def ANDBitSum(self,vec1,vec2):
        return vec1.minimum(vec2).sum()#vec1.dot(vec2.transpose()).sum()#vec1.minimum(vec2).sum()
        # alternatives:
        # return vec1*vec2.transpose()
        #return vec1.dot(vec2.transpose()).sum()

    def BitANDList(self,vec1,listVec):
        result = [0]*len(listVec)
        for i in range(len(listVec)):
            if listVec[i] is not None:
                result[i] = self.ANDBitSum(vec1,listVec[i])
            else:
                result[i] = 0

        return result

    def GetVecs(self,listStrings,data,appendMissing = False):
        res = []
        for s in listStrings:
            if s in data.keys(): # should not be needed, remove (!) ('2003-01' key error)
                res.append(data[s])
            else:
                if appendMissing is True: # only used for kommunkoder atm, remove after data update (!)
                    res.append(None)
        return res

    # takes out items in a vector based on the indices of a (binary) vec
    def GetFromBinaryVec(self,binaryVec,totalVec):
        # get all indexes
        tArray = np.nonzero(binaryVec)
        result = []

        for t in tArray[1]:
              result.append(totalVec[t])
        return result

class StructureInput:

    bitOps = BitOperations()

    # used in case '"' is in string
    def splitStringDetailed(self,s):
        list = []
        inExact = False
        sTot=""
        for i in range(0,len(s)):
            if s[i] == ' ' and inExact == False:
                list.append(sTot)
                sTot = ""
            else:
                if s[i] == '"':
                    inExact = not inExact
                else:
                    sTot = sTot+s[i]

        list.append(sTot)
        return list

    # splits string, treats "..." as one word - case sensitive
    def SplitAdd(self,s0,data,union = False):
        res = []
        if '"' in s0:
            list = self.splitStringDetailed(s0)
        else:
            list = s0.lower().strip().split(' ')
        current = []

        for s in list:
            if s is not ' ':
                if s in data:
                    vec = data[s]
                    res.append(vec)
                    print(s)

        if(len(res)>0):
            current = res[0]

            # these should be AND:ed or added/union together
            if len(res)>1:
                for i in range(1,len(res)):
                    if union == True:
                        current = self.bitOps.BitUnion(current,res[i])
                    else:
                        current = self.bitOps.BitAND(current,res[i])

        return current

    def SplitUnion(self,s0):

        unionParts = []
        xorParts = []
        currentString = ''

        for i in range(0,len(s0)):
            isUnion = False

            if s0[i] == '(':
                if currentString:
                    xorParts.append(currentString)
                currentString=''
                isUnion=True
            elif s0[i] == ')':
                if currentString:
                    unionParts.append(currentString)
                currentString=''
                isUnion=False
            else:
                currentString=currentString+s0[i]

        if currentString:
            xorParts.append(currentString)

        return [unionParts,xorParts]

    def Structure(self,s0,data):

        if '(' in s0 and ')' in s0:
            result = []
            a = self.SplitUnion(s0)
            unionParts = a[0]
            xorParts = a[1]
            currentVecXor = []
            currentVecUnion = []
            if len(unionParts)>0:
                currentVecUnion = self.SplitAdd(unionParts[0],data,True)
                for i in range(1,len(unionParts)):
                    vec = self.SplitAdd(unionParts[i],data,True)
                    currentVecUnion = self.bitOps.BitAND(currentVecUnion,vec)
            if len(xorParts)>0:
                currentVecXor = self.SplitAdd(xorParts[0],data,False)
                for i in range(1,len(xorParts)):
                    vec = self.SplitAdd(xorParts[i],data,False)
                    currentVecXor = self.bitOps.BitAND(currentVecXor,vec)
            # combine with xor
            resultVec = currentVecUnion
            combine = True
            if currentVecXor == []:
                combine = False
            if currentVecUnion == []:
                combine = False

            if combine:#len(currentVecXor)>0 and len(currentVecUnion)>0:
                resultVec = self.bitOps.BitAND(currentVecXor,currentVecUnion)

            return resultVec
        else:
            return self.SplitAdd(s0,data,False) # no union

    # get all independent inputs separately, separated by ','
    def getAllIndFromString(self,s,data):
        inds = []
        strs = []

        inExact = False
        sTot = ""
        for i in range(0,len(s)):
            if s[i]==',' and inExact==False:
                inds.append(self.Structure(sTot,data))
                strs.append(sTot)
                sTot = ""
            else:
                if s[i]=='"':
                    inExact = not inExact
                sTot=sTot+s[i]

        inds.append(self.Structure(sTot,data))
        strs.append(sTot)

        return [inds,strs]

    def GenerateVecs(self,s0,data):
        listIndependent = []
        listStrs = []
        # '(...)': combine
        # ',' : treat independently
        # ' ': xor
        # '"..."' treat all exactly as this

        if ',' in s0:
            #list = s0.split(',')
            #for s in list:
            #    listIndependent.append(self.Structure(s,data))
            #    listStrs.append(s)
            a = self.getAllIndFromString(s0,data)
            listIndependent = a[0]
            listStrs = a[1]
        else:
            listIndependent.append(self.Structure(s0,data))
            listStrs.append(s0)

        return [listIndependent,listStrs]


# Calculates Kullback-Leibler divergences
class KLCalculations:

    dataSparse = []
    sparseItem = []
    sparseItemComparison = []
    totNr = 0
    doComparison = False

    def calcUniqueKL(self,w):
        sparseWord = self.dataSparse[w]
        # calc KL values
        # AND + remove input from total
        andArray = self.sparseItem.minimum(sparseWord)
        andSum = andArray.getnnz() # takes time
        sparseItemRemoved = self.sparseItem - andArray

        yrkeNrElements = self.sparseItem.getnnz()

        p_i = float(andSum) / yrkeNrElements
        q_i = float(sparseItemRemoved.getnnz()) / self.totNr

        if(q_i<0.0000001 and p_i>0):
            d_i = p_i#KLdivSingle(p_i,q_i)
        else:
            d_i=0.0

        # append
        #klValues.append((w,d_i,p_i))
        return (w,d_i,p_i)

    def calcKL(self,w):
        sparseWord = self.dataSparse[w]

        #in case there is a comparison

        if self.doComparison == True:
            sparseWordComparison = sparseWord.minimum(self.sparseItemComparison)

        # calc KL values
        # AND
        # filtered = sparseYrke.multiply(sparseWord)
        andSum = self.sparseItem.minimum(sparseWord).getnnz() # this is what takes time
        yrkeNrElements = self.sparseItem.getnnz()

        p_i = float(andSum) / yrkeNrElements

        if self.doComparison == True:
            q_i = float(sparseWordComparison.getnnz()) / self.totNr
        else:
            q_i = float(sparseWord.getnnz()) / self.totNr

        if(q_i>0 and p_i>0):
            d_i = p_i*np.log(p_i/q_i)#KLdivSingle(p_i,q_i)
        else:
            d_i=0.0

        # append
        #klValues.append((w,d_i,p_i))
        return (w,d_i,p_i)

    def CalcSingle(self,sparseItem,data,words,totNr, sparseItemComparison = [], doUnique = False):

        self.dataSparse = data
        self.totNr = totNr
        self.sparseItemComparison = sparseItemComparison

        if self.sparseItemComparison != []:
            self.doComparison = True
            self.totNr = self.sparseItemComparison.getnnz()
        else:
            self.doComparison = False

        # get sparse vector
        self.sparseItem = sparseItem#data[input]
        klValues = []

        a = datetime.now()
        self.itemNrElements = self.sparseItem.getnnz()

        # map all words
        if doUnique == True:
            klValues = map(self.calcUniqueKL,words)
        else:
            klValues = map(self.calcKL,words)

        b = datetime.now()
        c=b-a
        print(c.total_seconds())

        klValues = sorted(klValues,key=lambda x: x[1],reverse=True)
        result = {}
        result['words'] = klValues
        return result

class GeneralOperations:

    data = [] # sparse vector data for each indexed word
    denseColumns = {} # dict with dense columnar data
    employer2SNIs = {}

    dataBitArrays = []
    currentBitVectors = []
    currentStrings = [] # get from structure input
    structureInput = StructureInput()
    bitOperations = BitOperations()
    klCalculations = KLCalculations()

    years = extraFunctions.GetAllYears()
    months = extraFunctions.GetAllMonths()
    occupations = extraFunctions.GetAllOccupations()
    kommunkoder = extraFunctions.GetAllKommunKoder()
    kommunNamn = extraFunctions.GetAllKommunNamn()

    yearVecs = []
    monthVecs = []
    occupationVecs = []
    kommunkodVecs = []

    resultYears = {}
    resultMonths = {}
    resultYrken = {}
    allResults = {}

    def __init__(self):
        self.data = []

    def ExistingWords(self,listStrings,data):
        result = []
        for s in listStrings:
            if s in data.keys():
                result.append(s)

        return result

#    def ConvertToBitArray(self,vec):
#        b=np.squeeze(np.asarray(vec))
#        # slow
#        bitA = bitarray.bitarray(len(b))
#
#        return 0

    def LoadData(self,filenameSparse,filenameDense,filenameSNIs=""):
        with gzip.open(filenameSparse + '.pklz', 'rb') as f:
            self.data = pickle.load(f, encoding='latin1')#cPickle.load(f)
        with gzip.open(filenameDense + '.pklz', 'rb') as f:
            self.denseColumns = pickle.load(f, encoding='latin1')#cPickle.load(f)

        if filenameSNIs != "":
            with open(filenameSNIs) as data_file:
                self.employer2SNIs = json.load(data_file)


        self.monthVecs = self.bitOperations.GetVecs(self.months,self.data)
        self.yearVecs = self.bitOperations.GetVecs(self.years,self.data)
        self.occupations = self.ExistingWords(self.occupations,self.data)
        self.occupationVecs = self.bitOperations.GetVecs(self.occupations,self.data)
        self.kommunkodVecs = self.bitOperations.GetVecs(self.kommunkoder,self.data,False)

        # also keep these as bit arrays
        #self.monthVecsBits = ConvertToBitArray(self.monthVecs);

    def ReadInput(self,s0):
        a = self.structureInput.GenerateVecs(s0,self.data)
        self.currentBitVectors = a[0]
        self.currentStrings = a[1]
        self.allResults.clear()
        for s in self.currentStrings:
            self.allResults[s] = {}

    def GetResults(self):
        return self.allResults

    def GetHistFromDense(self,name,vec,topNrs):
        dense = self.denseColumns[name]
        unordered = self.bitOperations.GetFromBinaryVec(vec,dense)
        res = extraFunctions.SortedHistogram(unordered,topNrs)

        return res

    def GetSNIsFromNames(self,names,weights):

        allSNIsCodes = []
        allSNIsNames = []
        for n in names:
            if n in self.employer2SNIs:
                for m in self.employer2SNIs[n]:
                    allSNIsCodes.append(m['Item1'])
                    allSNIsNames.append(m['Item2'])

        # make histogram
        res = extraFunctions.SortedHistogram(allSNIsCodes,1000)
        resNames = extraFunctions.SortedHistogram(allSNIsNames,1000)

        #hashRes = {}
        #for i in range(len(res[0])):
        #    hashRes[res[0][i]] = res[1][i]

        hashRes2 = {}
        hashRes2['Codes'] = res[0]
        hashRes2['x'] = resNames[0]
        hashRes2['y'] = res[1]

        return hashRes2

    def GetForOccupations(self):
        index = 0
        for vec in self.currentBitVectors:
            res = self.GetHistFromDense('yrke_id',vec,50)
            res = list(res)
            hashRes = {}
            hashRes['x'] = res[0]
            hashRes['y'] = res[1]

            # also remap to get all names
            self.allResults[self.currentStrings[index]]['occupations'] = hashRes
            index = index + 1

        #index = 0
        #for vec in self.currentBitVectors:
        #    res = self.bitOperations.BitANDList(vec[0],self.occupationVecs)
        #    hashRes = {}
        #    hashRes['Occupation'] = self.occupations
        #    hashRes['Counts'] = res
        #    self.allResults[self.currentStrings[index]]['occupations'] = hashRes
        #    index = index+1

    def GetForEmployers(self, generateSNIs=False):
        index = 0
        for vec in self.currentBitVectors:
            res = self.GetHistFromDense('arbetsgivare',vec,200)
            res = list(res) # python 3

            # optional, get
            if generateSNIs == True:
                hashSNI = self.GetSNIsFromNames(res[0],res[1])
                self.allResults[self.currentStrings[index]]['SNI'] = hashSNI

            hashRes = {}
            hashRes['x'] = res[0]
            hashRes['y'] = res[1]
            self.allResults[self.currentStrings[index]]['employers'] = hashRes
            index = index + 1

    def GetForKommuner(self):
        index = 0
        for vec in self.currentBitVectors:
            res = self.bitOperations.BitANDList(vec[0],self.kommunkodVecs)
            hashRes = {}
            hashRes['x'] = self.kommunkoder
            hashRes['y'] = res

            # also do per capita (dec 2015)
            resPerCapita = extraFunctions.GetKommunIdsPopulation(self.kommunkoder,res)
            hashRes['y_percapita'] = resPerCapita

            # change to make into dictionary
            dictRes = {}
            dictResTotal = {}
            for i in range(0,len(resPerCapita),1):
                dictRes[self.kommunkoder[i]] = resPerCapita[i]
                dictResTotal[self.kommunkoder[i]] = res[i]

            self.allResults[self.currentStrings[index]]['municipality_codes_percapita'] = dictRes
            self.allResults[self.currentStrings[index]]['municipality_codes_total'] = dictResTotal
            self.allResults[self.currentStrings[index]]['municipality_codes'] = hashRes

            index = index+1

    def GetForYears(self):
        index = 0
        for vec in self.currentBitVectors:
            res = self.bitOperations.BitANDList(vec[0],self.yearVecs)
            hashRes = {}
            hashRes['x'] = self.years
            hashRes['y'] = res
            self.allResults[self.currentStrings[index]]['years'] = hashRes
            index = index+1

    def GetForMonths(self):
        index = 0
        for vec in self.currentBitVectors:
            res = self.bitOperations.BitANDList(vec[0],self.monthVecs)
            hashRes = {}
            hashRes['x'] = self.months
            hashRes['y'] = res
            self.allResults[self.currentStrings[index]]['months'] = hashRes
            index = index+1

    # assumes single string
    def GetVecFromString(self,s0):
        a = self.structureInput.GenerateVecs(s0,self.data)
        if len(a[0]) == 0:
            return []
        else:
            return a[0][0] # maybe not [0]
        #self.currentBitVectors = a[0]
        #self.currentStrings = a[1]

    def KLSingle(self,input,inputComparison = "",doUnique=False):
        totNr = len(self.denseColumns['yrke_id'])
        words = self.data.keys()[0:20000]
        sparseItem = self.GetVecFromString(input)#self.data[input]
        sparseItemComparison = []
        if inputComparison != '':
            sparseItemComparison = self.GetVecFromString(inputComparison)#self.data[inputComparison]

        return self.klCalculations.CalcSingle(sparseItem,self.data,words,totNr,sparseItemComparison,doUnique)