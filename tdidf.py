import string
import math
from os import listdir
from os.path import isfile, join
import operator
from tabulate import tabulate
import wikipedia 
mypath = "./files"

with open(mypath+"/qualityFiles/stopWords.txt") as f:
    stopWords = f.read().splitlines()

def init():
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    listOfDict=[]
    for l in range(len(files)):
        listOfDict.append(count(files[l]))
    return listOfDict,files

def log10(nr):
    return math.log(nr,10)

def IDF(word,listOfDict,files):
    antallDoc = 0
    for dictonary in listOfDict:
        if dictonary.__contains__(word):
            antallDoc+=1
    return (log10( len(files) / (antallDoc+1) + 1 ))

def count(file):
    with open("files/"+file) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    dict = {}
    for line in content:
        for word in line.split():
            wordClean = ''.join(ch for ch in word if ch not in (string.punctuation+"1234567890-+_\n\t")).lower()
            if wordClean not in stopWords:
                if (len(wordClean)>=1):
                    if wordClean in dict:
                        dict[wordClean] += 1
                    else:
                        dict[wordClean] = 1
    return dict

def tdidf(q,docs,files):
    weights = []
    for x in range(len(docs)):
        row = []
        for word in q.split():
            if (docs[x].__contains__(word)):
                row.append((log10(1+docs[x][word])) * (IDF(word,docs,files)))
            else:
                row.append(0)
        weights.append(row)
    res=[]
    for rows in weights:
        res.append(sum(rows))
    return weights, res
def secondEl(a,b):
    return (a[1] > b[1]) - (a[1] < b[1])

def search(q):
    listOfDict,files = init()
    w,res = tdidf(q,listOfDict,files)
    prettyTab = []
    for textNR in range(len(files)):
        prettyTab.append([files[textNR],res[textNR]])
    return sorted(prettyTab, key=lambda tup: tup[1], reverse=True)
            