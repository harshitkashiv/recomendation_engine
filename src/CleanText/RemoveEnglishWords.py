
__author__="Harshit.Kashiv"

'''
This module provides functions for removing the most common English Words. 
To add any words edit commonEnglishWorsd.csv
'''
from RemoveHTMLContent import *
#Include the root directory in the path
import sys
sys.path.append('./../')

import pickle
import csv

import os

from pprint import pprint

import nltk

from string import digits

import HTMLParser

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

h = HTMLParser.HTMLParser()

def removeEnglishStopWordsAndClean(text):
    text = text.replace(':', ' ').replace(')', ' ').replace('(', ' ').replace(',', ' ').replace('.', ' ').replace('  ', ' ')
    text = text.replace('-', ' ').replace("'", " ")
    text = text.replace('?', ' ').replace('\\', ' ')
    text = text.translate(None,digits)
    text = text.replace("my bf","my boyfriend")
    text = text.replace("bf","breastfeeding")
    text = re.sub(" \d+", " ", text)
    text = text.replace("  "," ")
    
    word_list = text.lower().split(' ')
    
    '''Removing english stop words which are mentioned in the file:-commonEnglishWords.csv '''
       
    f = open("commonEnglishWords.csv","rU")
    result=csv.reader(f)
    commonWords=[]
    for row in result:
        commonWords.append(row[0].lower())
    
    filtered_words = [w for w in word_list if not w in commonWords]
    
    final_words=[]
    for w in filtered_words:
        if len(w)<20 and len(w) >2:
            final_words.append(w)
    
    text= ' '.join(final_words)

    return text

'''Lemmatization function'''
'''
def getLemmatizedText(text):
    print 'in'
    lemmaDictionary = pickle.load(open('CleanText/articleVocabAndLemma.pickle','rU'))
    lemmatized_words = []
    for word in text.split(' '):
        if word in lemmaDictionary:
            lemmatized_words.append(lemmaDictionary[word])
    print lemmatized_words
    return ' '.join(lemmatized_words)
     
    
def lemmatizeWords(text):
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    lt = WordNetLemmatizer()
    #word_list = text.lower().split(' ')
    lemmatized_words=[]
    print "In lemmatize words"
    for (word,tag) in tokens_pos:
        print word, tag
        try:
            if tag not in ("IN","CC","DT","UH","PRP$"):
                tag=get_wordnet_pos(tag)
                #print type(tag)
                #lemmatize_words.append(word)
                lemmatized_words.append(lt.lemmatize(word,tag))
        except:
            pass
        
#def stemWords(text):
 #   word_list = text.lower().split(' ')
  #  st = LancasterStemmer()
   # stemmed_words = [st.stem(word) for word in word_list]
    
    return ' '.join(lemmatized_words)


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
'''
def removeNull(text):
    word_list = text.lower().split(' ')
    filtered_words = [w for w in word_list if w!= ""]
    text= ' '.join(filtered_words)
    return text
    
def callRemoveHtml(data):
    ex = TextExtracter()
    ex.feed(data)
    text = ex.getvalue(ex)
    
    text = cleanText(text) 
    text = removeNull(text)
    text = h.unescape(text)
    #print "Text: ",text
    return text

if __name__=="__main__":
    
    data = "<a href=\"foo.com\" class=\"bar\">I Want uh with my a this that manager and organization and organize and managed and seemed and seem and worsen This <b>text!</b> < www.acb.com my email is rashi@gmail.com this mum is the url http://nonsense.com </a> print striphtml(data), manage., all man and men the words and dictionary"
    print data
    print type(data)
    text=callRemoveHtml(data)
    print type(text)
    print removeEnglishStopWordsAndClean(text)
    
