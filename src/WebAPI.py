
__author__="Harshit.Kashiv"

'''
This module provides webservice API for suggesting groups given a query
'''


import sys
sys.path.append('./../../')

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import time

print "Starting All Loads:", time.time()
import simplejson
from pprint import pprint
import traceback
import json

'''
from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect


import numpy as np


from operator import itemgetter

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from gensim import corpora, models, similarities

from CleanText.RemoveEnglishWords import callRemoveHtml,removeEnglishStopWordsAndClean

from TFIDF.createCorpus import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
'''

#from TFIDF.LoadMatricesSimilarity import gs

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

print_queries = False
print_responses = False

@app.route('/hello', methods = ['POST'])
def hello():
    #print request.__dict__
    content = request.get_json(force = True)
    print content
    print(request)
    #print content
    return "Hello World!"
    
@app.route('/requestedarticle', methods = ['POST'])
def requestedarticle():
    
    jsondata = request.get_json(force = True)
    jsondata = jsondata['article']
    
    
    try:
        sno = int(jsondata)
                          
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
        return 1
        #traceback.print_exc()
    
    return "Hello Wold!"    
        
@app.route('/suggestedarticles', methods = ['POST'])
def suggestedarticles():
    jsondata = request.get_json(force = True)
    
    try:
        sno = int(jsondata)
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


