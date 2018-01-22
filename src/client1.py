'''
Created on 14-March-2015

@author: Harshit Kashiv
'''

import urllib2

from pprint import pprint

import json

if __name__ == '__main__':
    url = 'http://127.0.0.1:3347/requestedarticle'
    url2 = 'http://127.0.0.1:3347/suggestedarticles'

#    url = 'http://0.0.0.0:3339/hello'
    
    #Define the user
#    user = {}
 #   user['userid'] = 1
  #  user['articleid'] = 'abs'
    
   # pprint(user)
    #jsondata = json.dumps(user)
    articleno = raw_input("Enter article no: ")
    jsondata = json.dumps({'article':int(articleno)})
    response = urllib2.urlopen(url, jsondata)
    jsonresp = response.read()
    response2 = urllib2.urlopen(url2, jsondata)
    jsonresp2 = response2.read()

    print jsonresp,"\n"
    print jsonresp2
    