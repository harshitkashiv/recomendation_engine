
__author__="Harshit.Kashiv"


'''
This module creates corpus(inpust format for tf_idf), calculates tf_idf
'''

#Include the root directory in the path
import sys
sys.path.append('./../')

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint

import csv

import time

from gensim import corpora, models, similarities

from CleanText.RemoveEnglishWords import callRemoveHtml,removeEnglishStopWordsAndClean

from GetArticlesData.getArticlesData2 import getArticlesData

from createCorpus import *

from operator import itemgetter

import traceback

def dedupeList(L, columnNum = 1):
    """
    This function sorts and dedupes a list based on a column
    """
    mydict = {} #Ordered dict would have been better here as per performance but is availaible for python2.7+ only
    for v in L: # where L is your list
        mydict[v[columnNum]] = v
    
    #Sort mydict based on keys -> reverse
    mydict2 = {}
    s = sorted(mydict.keys(), reverse = True)

    result = []
    for key in s:
        result.append(mydict[key])
    
    return result
    

class similarArticles:
    def __init__(self):
#        self.corpus = corpora.MmCorpus('articles_corpus.mm')
#        print self.corpus[1]
    #    self.dictionary=loadVocab()
     #   self.articles_data = createArticleWordFreq()
      #  self.corpus=createCorpus(self.articles_data,self.dictionary)
        #self.saveCorpus()
        
        self.snoToArticlesDict = (getArticlesData())[2]
        self.corpus = self.loadCorpus()
        # Creating corpus of texts
      #  self.corpus = corpora.MmCorpus('articles_corpus.mm')

#        self.corpus=createCorpus(self.articles_data,self.dictionary)
        self.tfidf = models.TfidfModel(self.corpus)
        self.tfidf_corpus= self.tfidf[self.corpus]
#        self.index = similarities.SparseMatrixSimilarity(self.tfidf_corpus, num_features=50000)
        self.lsi = models.LsiModel(self.tfidf_corpus, num_topics=300)
        self.index = similarities.MatrixSimilarity(self.lsi[self.tfidf_corpus])
        self.index.num_best = 20
        
                        
    def getArticleInfo(self,snoarticle):
        try:
            snoArticles = []
            snoArticles.append(int(snoarticle))
            articlesTitles = self.getArticlesTitles(snoArticles)
            print 'completed processing'
            return (articlesTitles)
        except:
            return
        
        
        
    def getSimilarArticles(self,snoarticle):
            
            
            print 'in the function'
#            print self.corpus[1]
            
           # lsi_query = self.lsi(corpus_tfidf_query)
            try:
                snoarticle = int(snoarticle)
                requestedArticle = self.getArticleInfo(snoarticle)
                corpus_tfidf_query=self.corpus[snoarticle]
      
#                corpus_tfidf_query=self.corpus.index(snoarticle)
                sim=self.index[self.lsi[corpus_tfidf_query]]
                
                sims = list(enumerate(sim))
                
    #            print sims
                
                sims1 = sorted(sims, key = lambda x: x[1][1], reverse= True)
                
                
  #              sims2 = dedupeScores(sims1)
                
   #             print sims2
                
    #            sims2 = sims2[:4]
                
     #           print sims2
                
      #          print 'sims2','\n', sims2
                
                sims3 = []
                for item in sims1:
                    if item[1][0] > snoarticle or item[1][0] < snoarticle:
                        sims3.append(item[1])
                
                
                snoArticles = []
                for item in sims3:
                    snoArticles.append(item[0])
                    
                
                articlesTitles = self.getArticlesTitles(snoArticles)
                articlesTitlesDeduped = dedupTitles(articlesTitles,requestedArticle)
 #               print 'articlesTitlesDeduped: ', articlesTitlesDeduped

                if len(articlesTitlesDeduped) <= 3:
                    articlesTitlesDeduped = articlesTitlesDeduped
                else:
                    articlesTitlesDeduped = articlesTitlesDeduped[:3]
                                
                print 'completed processing'
                
                return (articlesTitlesDeduped)
            except:
                traceback.print_exc()
                return

    
    def getArticlesTitles(self,snoArticles):
        #snoToArticlesDict = getArticlesData()[1]
        articlesTitles = []
        for item in snoArticles:
            articleTuple = (self.snoToArticlesDict[item]['article_title'],self.snoToArticlesDict[item]['article_url'])
            articlesTitles.append(articleTuple)
#            articlesTitles.append(self.snoToArticlesDict[item]['article_title'])
 #           articlesTitles.append(self.snoToArticlesDict[item]['article_url']) 
#            print self.corpus(item)           
 #           print self.snoToArticlesDict[item]['article_title']
  #          print self.snoToArticlesDict[item]['articleid']
   #         print self.snoToArticlesDict[item]['article_url']
        return articlesTitles

    def saveCorpus(self):
        with open('articlesCorpus.pickle','wb') as articlesCorpus:
            pickle.dump(self.corpus,articlesCorpus)
    
    def loadCorpus(self):
        corpus = pickle.load(open('articlesCorpus.pickle','rb'))
        return corpus
    

def dedupeScores(L):
    scoresDict = {}
    L2 = []
    for (intIndex, (articleId, score)) in L:
  #      print intIndex, articleId, score
        
        if score in scoresDict:
            pass
        else:
            scoresDict[score] = 1
            row = (intIndex, (articleId, score))
            L2.append(row)
            

    return L2

def dedupTitles(L,L1):
    titlesDict = {}
    L2 = []
    for (articleTitle, articleUrl) in L:
  #      print articleTitle, articleUrl
        if (articleTitle in titlesDict) or (articleTitle == L1[0][0]) or (articleTitle == '') or (articleUrl == ''):
            pass
        else:
            titlesDict[articleTitle] = 1
            row = (articleTitle,articleUrl)
            L2.append(row)
    
    return L2
     
 
if __name__=="__main__":
    ob1 = similarArticles()
    sno = raw_input("Enter the article number: ")
    print ob1.getSimilarArticles(sno)
    #ob1.saveCorpus()
    
    '''
    sno = raw_input("Enter the article number: ")
    print 'ob1.getArticleInfo(sno):', ob1.getArticleInfo(sno)
    print '\n'
    print ob1.getSimilarArticles(sno)
'''
    '''
    L = [(7, (47333, 0.74229389429092407)), (8, (42801, 0.74030834436416626)),\
          (9, (21954, 0.74212926626205444)), (9, (324253, 0.74212926626205444))]
    
    L = sorted(L, key = lambda x: x[1][1], reverse= True)
    
    print dedupeScores(L)

   '''
        
        
        
        
#get Articles Data

#Clean Articles Data

#Load Vocabulary

#create Corpus

#create Tfidf Matrix

#save TFidf Model

#take an article as an input

#calculate articles similarity

# send top-3 articles matching the given article

