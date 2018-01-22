
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

from Utils.Utils import getASCIIString, strip_tags

from CleanText.RemoveEnglishWords import *


class getArticlesData():
     
    def __init__(self):
        #1. Connect to MySQL database table wp_posts
        host="127.0.0.1"
        user="root"
        password="abcd@1234"
        database="tap_sg"
    
        self.mysql_conn = MySQLConnect(database, host, user, password)
        cmd = '''select * from wp_posts limit 2'''
        self.articles = self.mysql_conn.query(cmd)
        
        # Call Google API for Thai to English Translation
        
        API_KEY = "AIzaSyBGGfOdtKFhlJ1w2bitjsj194jUKIxoPT0"
        
        self.TRANSLATE_URL = "https://www.googleapis.com/language/translate/v2?key=" + API_KEY
        self.DETECT_URL = "https://www.googleapis.com/language/translate/v2/detect?key=" + API_KEY  # &q=google+translate+is+fast
        
    def unicode_urlencode(params):
        if isinstance(params, dict):
            params = params.items()
        return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])
        
        
    def make_request(url):
        return urllib.urlopen(url).read()
        
        
    def quick_translate(text, target, source):
        try:
            #print translate(text, target, source)
            return translate(text, target, source)["data"]["translations"][0]["translatedText"].replace('&#39;', "'")
        except:
            return ""
    
        
    def translate(text, target, source,self):
        query_params = {"q": text, "source": source, "target": target}
        url = self.TRANSLATE_URL + "&" + unicode_urlencode(query_params)
        try:
            return demjson.decode(make_request(url))
        except:
            return {}
            
    def quick_detect(text,self):
        try:
            lang= detect(text)["data"]["detections"][0][0]["language"]
            return lang
        except:
            return ""
    
    def detect(text):
        query_params = {"q": text}
        url = self.DETECT_URL + "&" + unicode_urlencode(query_params)
        try:
            return demjson.decode(make_request(url))
        except:
            return {}
            
    def getArticlesList(self):
    #2. Create a list of articles
        articlesDict = {} #article details
        snoToArticleDict = {} #sno -> article details
        articlesTitlesToDetailsDict = {} #article title -> article details
        articleText=[] # To store articles'text
        
        
        i=0
        
        for article in self.articles:
            
            article_title = article['post_title']
            article_content = article['post_content']
            
            if self.quick_detect(article_title)=="th":
                self.quick_translate(article_title,"en","th")
                self.quick_translate(article_content,"en","th")
            
            else:
                pass
                
            article_title = callRemoveHtml(article_title)
            articleid = article['ID']       
            article_url = article['guid']
            article_type = article['post_type']
            article_status = article['post_status']
            article_sno = i
            
            
         
            if (article_type == 'post') or (article_status == 'publish'): # Filtering only articles from database which are live
                
                article_title_with_space = ' ' + article_title
                
                ''' Creating text string with 5/6 weightage of title and 1/6 of article content'''
                
                article_text = article_content + article_title_with_space*5
                article_text = article_text.lower()
                article_text = getASCIIString(strip_tags(article_text))
                
                articleText.append(article_text)
                
                articleDetailsDict = {'article_text': article_text,
                                'articleid': articleid,
                                'article_title': article_title, 
                                'article_url': article_url,
                                'article_sno': article_sno
                                }
                
                articlesDict[articleid] = articleDetailsDict
                articlesTitlesToDetailsDict[article_title] = articleDetailsDict
                snoToArticleDict[i] = articleDetailsDict
                
                
                i += 1    
            else:
                pass    
            
           #5. Close the MySQL connection
        self.mysql_conn.close()
    
        return [articleText,articlesDict, snoToArticleDict, articlesTitlesToDetailsDict]
    

if __name__ == '__main__':    
    print 'Getting data of all articles from SQL', time.ctime()
    st_time = time.time()
    ga=getArticlesData()
    [articleText,articlesDict, snoToArticleDict, articlesTitlesToDetailsDict] = ga.getArticlesList()
    print articlesDict
    
   # print snoToArticleDict[12345]
        
    print 'Getting data of all articles from SQL....completed', time.ctime()
    
    print 'Time taken in fetching articles from SQL:', time.time() - st_time, ' seconds'

    