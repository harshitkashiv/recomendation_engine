'''
Created on 14-March-2015

@author: Harshit Kashiv
'''

import urllib2

from pprint import pprint

import json

if __name__ == '__main__':
    url = 'http://127.0.0.1:4242/ArticleRequested'
    url1 = 'http://127.0.0.1:4242/ArticleSimilarity'


#    url = 'http://0.0.0.0:3339/hello'
    
    #Define the user
#    user = {}
 #   user['userid'] = 1
  #  user['articleid'] = 'abs'
    
   # pprint(user)
    #jsondata = json.dumps(user)
#    data = ['sg_tap','week']
    jsondata = json.dumps({'articleno':1})
    response = urllib2.urlopen(url, jsondata)
    jsonresp = response.read()

    response = urllib2.urlopen(url1, jsondata)
    jsonresp1 = response.read()

    
    print jsonresp
    print jsonresp1
