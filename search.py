import os
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import math
import time
import nltk
import threading
from Stemmer import Stemmer
from collections import defaultdict, OrderedDict
from multiprocessing import Process
from os import mkdir
from bisect import bisect
try:    
    nltk.download('stopwords')
except:
    pass
import random
import sys

stop_words=set(stopwords.words('english'))
maxDocs=15000
documents=500000
stemmer = Stemmer('porter')
st=time.time()
f1=open("final1/secondary.txt","r")
secondaryIndexes=f1.readlines()
f1.close()

def tokenizer( wiki):
    wiki = re.sub(r'[^\x00-\x7F]+', ' ', wiki)
    wiki = re.sub(r'http\S+', '', wiki)
    wiki = re.sub('&amp;|&apos;|&gt;|&lt;|&nbsp;|&quot;', ' ', wiki)
    wiki = re.split(r"[^A-Za-z0-9]+", wiki)
    wiki = [stemmer.stemWord(w.lower())for w in wiki if not w.lower() in stop_words and len(
    w) < 45 and len(w) > 1]

    return wiki

def fetchPostList(word):
    pos=bisect(secondaryIndexes,word+"\n")-1 
    try:
        fileOpen=open("./final1/fin"+str(pos)+".txt","r")
    except:
        return -1
    fileOpen=open("./final1/fin"+str(pos)+".txt","r")
    fileReader=fileOpen.readline().replace("\n","")
    while fileReader:
        fileReader=fileReader.split(":")
        if fileReader[0]==word:
            return fileReader[1]
        fileReader=fileOpen.readline().replace("\n","")
    
    return -1

def getTitle(docId):
    fileId=docId//maxDocs
    file=open("./title/file"+str(fileId+1)+".txt","r")
    docId=docId%maxDocs
    title=""
    for i in range(docId+1):
        title=file.readline()

    return title.strip()

class Searching():
    def __init__(self) -> None:
        pass
    
    
    def numOfoccurences(self,tok):
        field_arr=["t","r","i","n","o","l"]
        list_=[]
        for i in field_arr:
            x=tok.find(i)
            y=""

            if x>0:
                x+=1
                length=len(tok)
                for ii in range(length):
                    if (ii+x)==length or tok[ii+x] in field_arr:
                        break
                    y+=tok[x+ii]
                list_.append(int(y,16))
            else:
                list_.append(0)
        return list_
# o=body
    def score(self,occurenceList):
        score_arr=[500,8,28,8,10,8]
        for i in range(len(occurenceList)):
            occurenceList[i]=occurenceList[i]*score_arr[i]
        return occurenceList

    def simpleSearch(self,data):
        data=tokenizer(data)
        scoreOfPages=defaultdict(int)
        field_arr=["t","r","i","n","o","l"]
        for word in data:
            occurences=fetchPostList(word)
            if occurences!=-1:
                countInFile=defaultdict(int)
                splitTokens=occurences.split("m")
                splitTokens=splitTokens[1:]
                idf=math.log2(documents/len(splitTokens)) # calculate idf
                
                for tok in splitTokens:
                    getPage=""
                    for i in tok:
                        if i not in field_arr:
                            getPage+=i
                        else:
                            break
                    getPage=int(getPage, 16)
                    occurenceList=self.numOfoccurences(tok)
                    scoreList=self.score(occurenceList)
                    for score in scoreList:
                        countInFile[getPage]+=score
                    scoreOfPages[getPage]+=math.log2(countInFile[getPage])*idf
        scoreOfPages= {k: v for k, v in sorted(scoreOfPages.items(), key=lambda item: item[1],reverse=True)}
        ans=""
        ii=0
        for i in scoreOfPages.keys():
            if(ii==10):
                break
            ii+=1
            x=str(i)
            x+=":"
            x+=getTitle(i)
            x+="\n"
            ans+=x
        if len(scoreOfPages)<10:
            for i in range(10-len(scoreOfPages)):
                num=random.randint(0,9820000)
                if num not in scoreOfPages.keys():
                    x=str(i);x+=":";x=getTitle(i);x+="\n";ans+=x
                else:
                    i-=1
        return ans


    def specialSearch(self,data):
        scoreOfPages=defaultdict(int)
        notSplitFirst=0
        dictStorer={}
        tokens=re.split(":",data)
        for tok in range(len(tokens)):
            if tok == 0:
                dictStorer[tokens[0]] = tokens[1].split(" ")
            elif(tok!=1):
                x = tokens[tok-1].split(" ")[-1:][0]  # t,c,b
                if(x in dictStorer):
                    if(tok == (len(tokens)-1)):
                        dictStorer[x].append(tokens[tok].split(" "))
                    else:
                        # print(tokens[tok].split)
                        dictStorer[x].append(tokens[tok].split(" ")[:-1])
                else:
                    if(tok == (len(tokens)-1)):
                        dictStorer[x] = tokens[tok].split(" ")
                    else:
                        dictStorer[x] = tokens[tok].split(" ")[:-1]           
        for x in dictStorer:
            dictStorer[x]=tokenizer(' '.join(dictStorer[x]))
        field_arr=["t","r","i","n","o","l"]
        converter_dict={"t":0,"r":1,"i":2,"c":3,"b":4,"l":5}
        # tok is t,r,i,n,o,l
        for token in dictStorer:
            for word in dictStorer[token]:    
                occurences=fetchPostList(word)
                if occurences!=-1:
                    countInFile=defaultdict(int)
                    splitTokens=occurences.split("m")
                    splitTokens=splitTokens[1:]
                    idf=math.log2(documents/len(splitTokens)) # calculate idf
                    for tok in splitTokens:
                        getPage=""
                        for i in tok:
                            if i not in field_arr:
                                getPage+=i
                            else:
                                break
                        getPage=int(getPage, 16)
                        occurenceList=self.numOfoccurences(tok)
                        scoreList=self.score(occurenceList)
                        scoreList[converter_dict[token]]=scoreList[converter_dict[token]]*15000 
                        for score in scoreList:
                            countInFile[getPage]+=score
                        scoreOfPages[getPage]+=math.log2(countInFile[getPage])*idf
        
        scoreOfPages= {k: v for k, v in sorted(scoreOfPages.items(), key=lambda item: item[1],reverse=True)}
        # ans=""
        # for i in range(0,min(10,len(scoreOfPages))):
        #     ans.append(str(scoreOfPages[i][0])+":"+self.extractTitle(scoreOfPages[i][0])+"\n")
        # print(ans)
        
        ans=""
        ii=0
        for i in scoreOfPages.keys():
            if(ii==10):
                break
            ii+=1
            x=str(i)
            x+=":"
            x+=getTitle(i)
            x+="\n"
            ans+=x
        if len(scoreOfPages)<10:
            for i in range(10-len(scoreOfPages)):
                num=random.randint(0,9820000)
                if num not in scoreOfPages.keys():
                    x=str(i);x+=":";x=getTitle(i);x+="\n";ans+=x
                else:
                    i-=1
        return ans


    def break_search(self,query):
        ans=""
        if(re.match(r"\w*[t|b|i|c|l|r]\s*:",query)):
            ans=self.specialSearch(query);
            
        else:
            ans=self.simpleSearch(query)
        return  ans

            
search=Searching()
file=open(sys.argv[1],"r")
lines=file.readlines()
file.close()
file=open(sys.argv[2],'w')
file.close()
file=open(sys.argv[2],'a')

for l in lines:
    start=time.time()
    ans=search.break_search(l)
    file.write(ans)
    file.write(str(time.time()-start)+" seconds\n\n")