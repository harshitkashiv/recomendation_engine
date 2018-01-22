
__author__="Harshit.Kashiv"


'''
This module create a list of articles which will be used as an input to tf-idf and lsi process
'''

#Include the root directory in the path
import sys
sys.path.append('./../')

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint

import time

from CleanText.RemoveEnglishWords import *

from GetArticlesData.getArticlesData2 import *


def createVocab():
        
    #ga = getArticlesData()
    #[articleText,articlesDict, snoToArticleDict, articlesTitlesToDetailsDict] =ga.getArticlesList()
    [articleText, articlesDict, snoToArticleDict, articlesTitlesToDetailsDict] = getArticlesData()

    complete_text = ''
    
    i = 0
    
    for element in articleText:
        text = callRemoveHtml(element)
        text_clean = removeEnglishStopWordsAndClean(text)
        complete_text = complete_text + " "+text_clean
        i+=1
        if i%10000 == 0:
            print 'Records Cleaned', i
        
    #print complete_text
    i=0    
    j=1
    allKeywordsDict = {}
    
    for word in complete_text.split(' '):
        
        if word=="" or word==" ":
            continue
        #print word
            #Search for the unigrams
        if word in allKeywordsDict:
            allKeywordsDict[word][1]+= 1
        else:
            allKeywordsDict[word] = [i,j]
            i=i+1
    
    for key,value in allKeywordsDict.items():
        if value[1] < 3:
            del allKeywordsDict[key]
    
    print len(allKeywordsDict) , 'words'
    return allKeywordsDict

dict = createVocab()
#print dict

g1 = open('articleVocabDictionaryWithoutLemma.csv','wb')

writer_g1 = csv.writer(g1)

for key, value in dict.items():
    row = [key,value[0],value[1]]
    writer_g1.writerow(row)

g1.close()



