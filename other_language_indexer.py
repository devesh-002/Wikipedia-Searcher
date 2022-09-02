import os
import re
import sys
from turtle import title
import xml.sax
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import threading
import time
import nltk
import threading
from Stemmer import Stemmer
from collections import defaultdict, OrderedDict
from multiprocessing import Process
from os import mkdir

totalInvertedTokens = 0
stop_words=set()
with open('hindi_stopwords.txt', 'r') as f:
	stop_words = {word.strip() for word in f}
stem_words=set()
with open('hindi_stemwords.txt', 'r') as f:
	stem_words = {word.strip() for word in f}
    
# try:
#     nltk.download("stopwords")
# except:
#     pass

try:
    mkdir(sys.argv[2])
except:
    pass
try:
    mkdir("other_title")
except:
    pass
title_arr = []
max_tokens = 15000
max_docs = 1500
index = defaultdict(list)
filecount = 0
total_tokens = 0
st = time.time()


class TextProcessing():
    def __init__(self) -> None:
        pass

    # def stop_word_removal(self, wiki):
    #     return [stemmer.stemWord(w)for w in wiki if not w.lower() in stop_words and len(w) < 45 and len(w) > 1]

    # def stemming(self, wiki):
    #     ans = []
    #     for w in wiki:
    #         ans.append(stemmer.stemWord(w))
    #     return ans

    def tokenizer(self, wiki):
        wiki = re.sub(r'http[s]?\S*[\s | \n]', r' ', wiki) # removing urls
        wiki = re.sub(r'\{.?\}|\[.?\]|\=\=.*?\=\=', ' ', wiki)
        clean = ''.join(ch if ch.isalnum() else ' ' for ch in wiki)
        clean = clean.split()
    	
        global total_tokens
        # wiki = re.split(r"[^A-Za-z0-9]+", wiki)
        total_tokens += len(clean)
        # wiki = [stemmer.stemWord(w)for w in wiki if not w.lower() in stop_words and len(
        #     w) < 45 and len(w) > 1]
        final=[]
        for w in clean:
            if w in stop_words or len(w)>45 or len(w)==1:
                continue
            else:
                for stm in stem_words:
                    if(w.endswith(stm)):
                        w=w[:-len(stm)]
                final.append(w)

        return final

    def preProcessText(self, wiki):
        wiki = self.tokenizer(wiki)

        return wiki

    def processCategories(self, wiki):

        list_of_cats = []
        list_of_cats = re.findall(r'\[\[category:(.*)\]\]', wiki)
        ans = self.preProcessText(' '.join(list_of_cats))
        return ans

    def processBody(self, text):

        data = re.sub(r'\{\{.*\}\}', r' ', text)
        processed_text = self.preProcessText(data)

        return processed_text

    def processExternalLinks(self, wiki):

        arr = re.split("== *external links *==", wiki)
        ans = []
        if(len(arr) > 1):
            data = arr[1]
            ans = re.findall(r'\*\s*\[\s*(.*)\]*', data)
        final_ans = self.preProcessText(' '.join(ans))

        return final_ans

    def processInfobox(self, wiki):
        ans = []
        line_by_line = re.split("\n", wiki)
        check_if_end = False
        for read_line in line_by_line:
            matchChecker = re.match(r'\{\{infobox', read_line)
            if check_if_end == True:
                if(read_line == "}}"):
                    check_if_end = False
                    continue
                else:
                    ans.append(read_line)

            if(check_if_end == False and matchChecker == True):
                check_if_end = True
                x = re.sub(r"\{\{infobox(.*)", r"\1", read_line)
                ans.append(x)

        ans = self.preProcessText(" ".join(ans))
        return ans

    def extractTitle(self, wiki):
        return(self.preProcessText(wiki))

    def processReferences(self, wiki):

        ans = []
        reference_list = re.findall(r' *title[^\|]*', wiki)

        for i in reference_list:
            ans.append(i.replace('title', '', 1))
        within_info = self.preProcessText(' '.join(ans))
        return within_info

    def process_entire_text(self, wiki, title):
        wiki = wiki.lower()
        title = title.lower()
        global filecount
        global title_arr
        seperator = re.split(r"== *references *==", wiki)
        references = []
        externalLinks = []
        categories = []
        infoBox = []
        body = []

        if(len(seperator) > 1):

            externalLinks = self.processExternalLinks(seperator[1])

            categories = self.processCategories(seperator[1])

            references = self.processReferences(seperator[1])
        infoBox = self.processInfobox(seperator[0])
        body = self.processBody(seperator[0])
        title_arr.append(title.lower())
        title = self.extractTitle(title)

        return title, body, infoBox, categories, externalLinks, references


def printInANewFile():
    global title_arr
    global indexList
    global totalInvertedTokens
    global filecount
    print(filecount)
    name = "./"+sys.argv[2]+"/file" + str(filecount) + ".txt"
    file = open(name, "w")
    x = OrderedDict(sorted(indexList.items(), key=lambda t: t[0]))
    for word in x.keys():
        s = word + ":"
        str_stored = indexList[word]
        s += str_stored
        file.write(s+"\n")
    file.close()

    titlename = "./title/file"+str(filecount)+".txt"
    file = open(titlename, "w")
    for word in title_arr:
        file.write(word)
    file.close()
    title_arr = []
    totalInvertedTokens += len(indexList)
    indexList = {}
    filecount += 1



class IndexText():
    def __init__(self, title, category, body, links, reference, infobox):

        self.title = title
        self.category = category
        self.body = body
        self.links = links
        self.reference = reference
        self.infobox = infobox

    def index_creater_func(self):
        title = {}
        body = {}

        global pageCount
        global indexList
        links = []
        reference = []
        infobox = []

        all_words = defaultdict(int)
        title_dict = defaultdict(int)
        for i in self.title:
            title_dict[i] += 1
            all_words[i] += 1
        body_dict = defaultdict(int)
        for i in self.body:
            body_dict[i] += 1
            all_words[i] += 1

        info_dict = defaultdict(int)
        for i in self.infobox:
            info_dict[i] += 1
            all_words[i] += 1

        category_dict = defaultdict(int)
        for i in self.category:
            category_dict[i] += 1
            all_words[i] += 1

        links_dict = defaultdict(int)
        for i in self.links:
            links_dict[i] += 1
            all_words[i] += 1

        reference_dict = defaultdict(int)
        for i in self.reference:
            reference_dict[i] += 1
            all_words[i] += 1
        count = 0
        for word in all_words:

            s = "m"+f'{pageCount:x}'

            if word in title_dict:
                s += "t"+f'{title_dict[word]:x}'

            if word in reference_dict:
                s += "r"+f'{reference_dict[word]:x}'

            if word in info_dict:
                s += "i"+f'{info_dict[word]:x}'

            if word in category_dict:
                s += "n"+f'{category_dict[word]:x}'

            if word in body_dict:
                s += "o"+f'{body_dict[word]:x}'

            if word in links_dict:
                s += "l"+f'{links_dict[word]:x}'

            if word in indexList:

                indexList[word] += (s)
            else:
                indexList[word] = s
            count += 1

        pageCount += 1
        if(pageCount % max_docs == 0):
            printInANewFile()


class PageHandler(xml.sax.ContentHandler):

    global pageCount

    def __init__(self):
        self.CurrentData = ''
        self.title = ''
        self.text = ''
        self.data = ''

    def characters(self, content):
        if self.CurrentData == 'title':
            self.title += content
        elif self.CurrentData == 'text':
            self.text += content

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        global st
        global titlearr
        if tag == 'page':
            global pageCount
            global filecount
            check = TextProcessing()
            title, body, infobox, categories, links, references = check.process_entire_text(
                self.text, self.title)

            indexClass = IndexText(
                title, categories, body, links, references, infobox)
            indexClass.index_creater_func()

            self.text = ''
            self.title = ''
            self.CurrentData = ""


global indexList
indexList = {}
global words

pageCount = 0
f1 = sys.argv[1]
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler(Handler)
parser.parse(f1)
printInANewFile()
et = time.time()
total = et - st
print('Execution time:', total, 'seconds')

with open(sys.argv[3], "w") as fp:
    fp.write(str(total_tokens)+"\n")
    fp.write(str(totalInvertedTokens)+"\n")
