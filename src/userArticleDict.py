
__author__="Harshit.Kashiv"



#Include the root directory in the path
import sys
sys.path.append('./../')

import pymongo

from DataConnections.MongoConnect.MongoConnect import MongoConnect

from pprint import pprint

from datetime import datetime

import time

import pickle



def createUserData():
    # Connecting to user log table from which data needs to be retreived
    monconn_get=MongoConnect("users",database="capi_logs")
    monconn_cur=monconn_get.getCursor()
    
    i=0
    userarticleDict={}
    
    for user in monconn_cur.find():
        userid=user["userid"]
        articleid=user["articleid"]
        date_str=user["_id"].generation_time.strftime('%m/%d/%Y')
        
        date=datetime.strptime(date_str,"%m/%d/%Y")
        days=(datetime.now()-date).days
        
          
        if i%10000==0:
            print i
            
        i+=1
        
        #print days
        if days>90:
            continue
 
    
        if userid is None:
            continue
        
        if userid in userarticleDict:
            if articleid in userarticleDict[userid]:
                continue
            else:
                userarticleDict[userid].append(articleid)
        else:
            userarticleDict[userid]=[]
            userarticleDict[userid].append(articleid)    
    
    return userarticleDict

    
        
    

if __name__=="__main__":
    userarticleDict=createUserData()
    print "user article Dict"
    with open("userarticleDict.pickle","wb") as userData:
        pickle.dump(userarticleDict,userData) 
                