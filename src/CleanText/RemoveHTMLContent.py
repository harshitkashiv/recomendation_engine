
__author__="Harshit.Kashiv"


'''
This module provides functions for cleaning texts by removing htl contents
'''

#Include the root directory in the path
import sys

import csv

import re

import os

from pprint import pprint

import nltk

from urlparse import urlparse

from nltk.stem.lancaster import LancasterStemmer

from sgmllib import SGMLParser


class TextExtracter(SGMLParser):
    """
    This class takes care of html
    """
    def __init__(self):
        self.text = []
        SGMLParser.__init__(self)
    def handle_data(self, data):
        self.text.append(data)
    def getvalue(self,ex):
        return ''.join(ex.text)




def removeEmailIDs(text):
    """This function removes email ids from text"""
    word_list = text.lower().split(' ')
    
    
    filtered_words = [ x for x in word_list if re.findall(r'[\w\.-]+@[\w\.-]+', x)== [] ]
    
    return ' '.join(filtered_words)
    
    
def removeUrl(text):
    """This function remove url from the text"""
    word_list = text.lower().split(' ')
    
    filtered_words=[]
    for el in word_list:
        try:
            if not urlparse(el).scheme:
                filtered_words.append(el)
        except:
            pass
    
    return ' '.join(filtered_words)

"""def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)"""

def removeSpecialCharacters(text):
    
    lines = text.split("\n")
    text =""
    for line in lines:
        #print line
        word_list = line.split(" ")
        pattern=re.compile("[^\w']")
        filtered_words = [ pattern.sub(' ', x) for x in word_list ]
        text = text +" "+' '.join(filtered_words)
    text = text.replace("  "," ")
    text = text.replace("  "," ")
    
    return text

def cleanText(text):
    
    text = removeUrl(text)
    text = removeWWW(text)
    text = removeEmailIDs(text)
    text = removeSpecialCharacters(text)
    return text

def removeWWW(text):
    word_list = text.split(" ")
    
    filtered_words = [ re.sub(r'^www.*[\r\n]*', '', x) for x in word_list ]
    filtered_words = [ x.replace("  "," ") for x in filtered_words ]
    
    
    return ' '.join(filtered_words)

if __name__ == "__main__":
    #print removeUrl("hello my my@gmail.com ftp://nonsense.com")
    data = "<a href=\"foo.com\" class=\"bar\">I Want This <b>text!</b> www.acb.com my email is rashi@gmail.com this is the url http://nonsense.com </a>"
    """print striphtml(data)"""
    print data
    ex = TextExtracter()
    ex.feed(data)
    text = ex.getvalue(ex)
    
    print cleanText(text)
    
    