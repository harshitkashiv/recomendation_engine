
__author__="Harshit.Kashiv"
s

'''
This module create a list of articles which will be used as an input to tf-idf and lsi process
'''

#Include the root directory in the path
import sys
sys.path.append('./../')
import pickle
from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint

import time

from gensim import corpora, models, similarities
#from nltk.stem.lancaster import LancasterStemmer

from CleanText.RemoveEnglishWords import *

from GetArticlesData.getArticlesData2 import *

import nltk

from string import digits

from nltk.stem.lancaster import LancasterStemmer


from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet


def loadVocab():
    vocab = {}
    file = 'articleVocabDictionaryWithoutLemma.csv'
    f = open(file,"rU")
    f_reader = csv.reader(f, delimiter=',')
    i = 0
    for line in f_reader:
        vocab[line[0]] = i
        i += 1
    f.close()
    return vocab

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizeWords(text):
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    lt = WordNetLemmatizer()
    
    lemmatized_word = '1'
    
    for (word,tag) in tokens_pos:
        if tag not in ("IN","CC","DT","UH","PRP$"):
            tag=get_wordnet_pos(tag)
            lemmatized_word = lt.lemmatize(word,tag)
        
    return lemmatized_word


def createLemmaDict(vocab):
    lemmaDict = {}
    for key in vocab:
        lemmaDict[key] = lemmatizeWords(key)
    return lemmaDict
        

if __name__=="__main__":
    vocab={'managing':0,'manager':0,'computer':1,'user':2,'the':2}
    lemmadictionary = createLemmaDict(loadVocab())
    #print lemmadictionary
   
    """
    g1 = open('articleVocabAndLemma2.csv','wb')

    writer_g1 = csv.writer(g1)

    for key, value in lemmadictionary.items():
        if value not in '1':
            row = [key,value]
            writer_g1.writerow(row)
    
    g1.close()
    """
    with open('articleVocabAndLemma.pickle','wb') as articleVocabAndLemma:
       pickle.dump(lemmadictionary,articleVocabAndLemma)
    
    

    