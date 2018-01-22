
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

def getArticlesData():
    
    #1. Connect to MySQL database table wp_posts
    host="127.0.0.1"
    user="root"
    password="abcd@1234"
    database="tap_sg_new"

    mysql_conn = MySQLConnect(database, host, user, password)
    cmd = '''select * from wp_posts'''
    articles = mysql_conn.query(cmd)
   
    #2. Create a list of articles
    articleText = []
    articlesDict = {} #article details
    snoToArticleDict = {} #sno -> article details
    articlesTitlesToDetailsDict = {} #article title -> article details
    
    
    i=0
    
    for article in articles:

        article_content = article['post_content']
        articleid = article['ID']       
        article_title = article['post_title']
        article_title = callRemoveHtml(article_title)
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
    mysql_conn.close()
    
    return [articleText, articlesDict, snoToArticleDict, articlesTitlesToDetailsDict]
    

if __name__ == '__main__':    
    print 'Getting data of all articles from SQL', time.ctime()
    st_time = time.time()
    
    pattern = re.compile('jpg')
    m = re.search('jeg','abcdef_123#$.jpeg')
    m1 = re.search('jeg','abcdef_123#$.jpeg')
    if m is not None or m1 is not None:
        print "m is none"
    else:
        print "m.group(0)"
    [articleText, articlesDict, snoToArticleDict, articlesTitlesToDetailsDict] = getArticlesData()
    
    print snoToArticleDict[1234]
        
    print 'Getting data of all articles from SQL....completed', time.ctime()
    
    print 'Time taken in fetching articles from SQL:', time.time() - st_time, ' seconds'

    