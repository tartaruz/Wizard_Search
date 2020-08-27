import string
import math
from os import listdir
from os.path import isfile, join
import operator
from tabulate import tabulate
import wikipedia 
mypath = "files"


def log10(nr):
    return math.log(nr,10)

def IDF(word):
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
            if (len(wordClean)>=1):
                if wordClean in dict:
                    dict[wordClean] += 1
                else:
                    dict[wordClean] = 1
    return dict

def tdidf(q,docs):
    weights = []
    for x in range(len(docs)):
        row = []
        for word in q.split():
            if (docs[x].__contains__(word)):
                row.append((log10(1+docs[x][word])) * (IDF(word)))
            else:
                row.append(0)
        weights.append(row)
    res=[]
    for rows in weights:
        res.append(sum(rows))
    return weights, res

def init():
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    listOfDict=[]
    for l in range(len(files)):
        listOfDict.append(count(files[l]))
    return listOfDict,files

q = None
while q!="exit":
    

    q = input(str("\nQuery? : "))
    if q=="data+":
        try:
            print("\n-------------Adding page to files-----------")
            subject = str(input("Subject = ")).lower()
            dataWiki = wikipedia.page(subject).content
            f = open("files/"+subject+".txt", "w")
            f.write(dataWiki)
            f.close()
            print("Added file "+subject)
        except:
            print("No match in wikipedia")
        print("\n----------End Adding page to files-----------")
    else:
        listOfDict,files = init()
        w,res = tdidf(q,listOfDict)
        max_index, max_value = max(enumerate(res), key=operator.itemgetter(1))
        if sum(res)!=0 :
            prettyTab = []
            for textNR in range(len(files)):
                prettyTab.append([files[textNR],res[textNR]])
            print(tabulate(prettyTab, headers=['Name', 'Result']))
            print("Document \""+files[max_index]+"\" is the most relevant")
        else:
            print("No match")
            
