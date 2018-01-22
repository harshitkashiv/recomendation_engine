
__author__="Harshit.Kashiv"


'''
This module create a list of articles which will be used as an input to tf-idf and lsi process
'''

#Include the root directory in the path
import sys
sys.path.append('./../')

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint
import pickle
import time

from gensim import corpora, models, similarities
#from nltk.stem.lancaster import LancasterStemmer

from CleanText.RemoveEnglishWords import *

from GetArticlesData.getArticlesData2 import *

def loadVocab():
    
    vocab = {}
    
    lemmatizedDict = pickle.load(open("articleVocabAndLemma.pickle","rb"))
    
    i=0
    for original, lemmatized in lemmatizedDict.items():
        if lemmatized in vocab:
            pass
        else:
            vocab[lemmatized] = i
            i+=1
    
    with open('articlesVocabLemmaIndex.pickle','wb') as articlesVocab:
        pickle.dump(vocab,articlesVocab)
    
    #lemmaIndex = pickle.load(open('articlesVocabLemmaIndex.pickle','rU'))
    return lemmaIndex
    
def createArticleWordFreq():
 
    data_complete = getArticlesData()
    snoToArticleDict = data_complete[2]
    data = []
    for i in range(len(snoToArticleDict)):
        data.append(snoToArticleDict[i]['article_text'])
  #  vocab = loadVocab()
    lemmatizedDict = pickle.load(open("articleVocabAndLemma.pickle","rb"))
    articlesWordFreq = []
    for article in data:
        dict = {}
        for word in article.split(' '):
            if word in lemmatizedDict:                
                word_lemmatized = lemmatizedDict[word]
                if word_lemmatized in dict:
                    dict[word_lemmatized] += 1
                else:
                    dict[word_lemmatized] = 1
            else:
                pass
        articlesWordFreq.append(dict)
    with open('articlesWordFrequency.pickle','wb') as articlesWordFrequency:
        pickle.dump(articlesWordFreq,articlesWordFrequency)
#    return articlesWordFreq
#    articlesWordFreq = pickle.load(open('articlesWordFrequency.pickle','rU'))      
    return articlesWordFreq
    

def createCorpus(articlesWordFreq,lemmaDict):
    corpus=[]
    for text in articlesWordFreq:
        article_list=[]
        for word in text:
            if word in lemmaDict:
                #print (word,dictionary[word],text[word])
                tuple=(lemmaDict[word],text[word])
                article_list.append(tuple)
            else:pass
        corpus.append(article_list)
    return corpus


if __name__=="__main__":
    articlesWordFreq=[{'human':1,'computer':2},{'survey':3,'user':2}] 
    lemmaDict={'human':0,'computer':1,'user':2}
 #   corpus= createCorpus(articles,vocab)
  #  articlesWordFreq = createArticleWordFreq()
    """
    print corpus
    tfidf=models.TfidfModel(corpus)
    vec=[[(1,1),(0,1)],[(1,2)]]

    print(tfidf[vec])
    for i in tfidf[vec]:
        print i
    
    """
    articlesWordFreq = createArticleWordFreq()
#    print articles
 #   print len(articles)
    lemmaDict = loadVocab()
    #print vocab
    corpus = createCorpus(articlesWordFreq, lemmaDict)
  #  print len(corpus)
    
    corpora.MmCorpus.serialize('articles_corpus.mm', corpus)
#    corpus = corpora.MmCorpus('articles_corpus.mm')
 #   for i in range(1):
  #      print corpus[i]
        
    