
__author__="Harshit.Kashiv"


'''
This module provides webservice API for suggesting groups given a query
'''


import sys
sys.path.append('./../')

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint

import numpy as np

import time

from operator import itemgetter

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

import csv

import time

from gensim import corpora, models, similarities

from CleanText.RemoveEnglishWords import callRemoveHtml,removeEnglishStopWordsAndClean
                                                                                                                                                                                                                                                    
from TFIDF.createCorpus import *

from operator import itemgetter

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from LoadMatricesSimilarity import gs

import web

import json

urls = (

    '/ArticleSimilarity','ArticleSimilarity', '/ArticleRequested', 'ArticleRequested'


    )

app = web.application(urls, globals())


class ArticleRequested:
    def POST(self):
        data = json.loads(web.data())
        query = data['articleno']
        
        try:
            sno = int(query)
                              
            ArticleReq = gs.getArticleInfo(sno)
            str = ''
            i = 0
            for (item1,item2) in ArticleReq:
                if i == 0 :
                    str = str+item1 + ',,,' + item2
                else:
                    str = str + ',,,' + item1 + ',,,' + item2
                i+= 1
            return str
        except:
            return
        

class ArticleSimilarity:
    def POST(self):
        data = json.loads(web.data())
        query = data['articleno']

        try:
            sno = int(query)
            similarArticles = gs.getSimilarArticles(sno)
            print similarArticles
            str = ''
            i = 0
            for (item1,item2) in similarArticles:
                if i == 0 :
                    str = str+item1 + ',,,' + item2
                else:
                    str = str + ',,,' + item1 + ',,,' + item2
                i+= 1
                print str
            return str
        except:
            return


if __name__ == "__main__":
    app.run()