
__author__="Harshit.Kashiv"


'''
This module provides functions for removing the most common English Words. 
To add any words edit commonEnglishWorsd.csv
'''
from RemoveHTMLContent import *
#Include the root directory in the path
import sys

import csv

import os

from pprint import pprint

import nltk

from string import digits

from nltk.stem.lancaster import LancasterStemmer


from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet

def removeEnglishStopWordsAndClean(text, englishStopWordsFilename):
    text = text.replace(':', ' ').replace(')', ' ').replace('(', ' ').replace(',', ' ').replace('.', ' ').replace('  ', ' ')
    text = text.replace('-', ' ').replace("'", " ")
    text = text.replace('?', ' ').replace('\\', ' ')
    text = text.translate(None,digits)
    text = text.replace("my bf","my boyfriend")
    text = text.replace("bf","breastfeeding")
    text = re.sub(" \d+", " ", text)
    text = text.replace("  "," ")
    
    word_list = text.lower().split(' ')
    
    f = open(englishStopWordsFilename,"rU")
    result=csv.reader(f)
    commonWords=[]
    for row in result:
        commonWords.append(row[0].lower())
    
    filtered_words = [w for w in word_list if not w in commonWords]
    
    final_words=[]
    for w in filtered_words:
        if len(w)<20 and len(w) >2:
            final_words.append(w)
            
    """st = LancasterStemmer()
    stemmed_words = [st.stem(word) for word in filtered_words]"""
    #print stemmed_words
    text= ' '.join(final_words)
    #print text
    #print "Stemmed: ",stemWords(text)
    text = lemmatizeWords(text)
    return text


def lemmatizeWords(text):
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    lt = WordNetLemmatizer()
    #word_list = text.lower().split(' ')
    lemmatized_words=[]
    
    for (word,tag) in tokens_pos:
        if tag not in ("IN","CC","DT","UH","PRP$"):
            tag=get_wordnet_pos(tag)
            #print type(tag)
            #lemmatize_words.append(word)
            lemmatized_words.append(lt.lemmatize(word,tag))
        
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

def removeNull(text):
    word_list = text.lower().split(' ')
    filtered_words = [w for w in word_list if w!= ""]
    text= ' '.join(filtered_words)
    return text
    
def stripHTMLTags(text):
    ex = TextExtracter()
    ex.feed(text)
    text = ex.getvalue(ex)
    
    text = cleanText(text) 
    text = removeNull(text)
    #print "Text: ",text
    return text

if __name__=="__main__":
    
    data = "<a href=\"foo.com\" class=\"bar\">I Want uh with my a this that manager and organization and organize and managed and seemed and seem and worsen This <b>text!</b> < www.acb.com my email is rashi@gmail.com this mum is the url http://nonsense.com </a> print striphtml(data), manage., all man and men the words and dictionary"
    print data
    print type(data)
    text=callRemoveHtml(data)
    print type(text)
    print removeEnglishStopWordsAndClean(text)
    
