__author__="Harshit.Kashiv"



#Include the root directory in the path
import sys
sys.path.append('./../')

import pymongo

from DataConnections.MySQLConnect.MySQLConnect import MySQLConnect

from pprint import pprint

import time

class MongoConnect():
    def __init__(self, table,database = 'capi_logs', host = 'localhost', port = 27017):
        #Used all times except when first table is created

        #Make a mongodb connection
        self.connection = pymongo.Connection(host, port)

        #self.connection = pymongo.mongo_client.MongoClient(host,port) #Works with pymongo2.4+
        self.table = self.connection[database][table] #test_cja is the db name
    

    def doIndexing(self, table, indexFields, database = 'capi_logs', host = 'localhost', port = 27017, ukey = True):
        #Index some of the fields
        if ukey == False:
            self.table.ensure_index(indexFields)
        else:
            args = {'unique':'true'}
            self.table.ensure_index(indexFields, **args)

    def saveToTable(self, document):
        self.table.save(document)

    def loadFromTable(self, myCondition):
        #print myCondition
        cur = self.table.find(myCondition)
        rows = list(cur)
        return rows
    
    def loadFromTableGeneric(self, myCondition1, myCondition2):
        #print myCondition
        cur = self.table.find(myCondition1, myCondition2)
        rows = list(cur)
        return rows

    def getCursor(self):
        cur = self.table
        return cur

    def dropTable(self):
        self.table.drop()

    def subsetTable(self, table, database = 'capi_logs', host = 'localhost', port = 27017):
        #Subset the table to retrieve the data of  a chunk
        s = {'id': { '$mod': [ 4, 0 ] } }
        cur = self.table.find(s)
        rows = list(cur)
        return rows

    def getLastRecord(self):
        args = {'_id':'-1'}
        s = self.table.find().sort([('_id', pymongo.DESCENDING)]).limit(1)
        lastRow = list(s)
        return lastRow

    def getLastRecordByAutoID(self):
        args = {'autoid':'-1'}
        s = self.table.find().sort([('autoid', pymongo.DESCENDING)]).limit(1)
        lastRow = list(s)
        return lastRow

    def close(self):
        self.connection.close()

    def saveOrUpdateToTable(self, myCondition, document):
        self.table.update(myCondition, document, upsert = True)
        
    def saveOrUpdateToTableFields(self, myCondition, document, multi = False):
        self.table.update(myCondition, document, upsert = True,multi=multi)
    
    def removeDocument(self, myCondition):
        self.table.remove(myCondition)

    def __del__(self):
        self.connection.close()


if __name__=="__main__":


    # Connecting to user table to be populated
    indexFields = [('userid',pymongo.ASCENDING)]
    monconn=MongoConnect("userData",database="capi_logs")
    monconn.doIndexing("userData", indexFields)
    
    
    # Connecting to user log table from which data needs to be retreived
    monconn_get=MongoConnect("users",database="capi_logs")
    monconn_cur=monconn_get.getCursor()
    
    i=0
    
    for user in monconn_cur.find():
        userid=user["userid"]
        articleid=user["articleid"]
        
        if i%10000==0:
            print i
        
        i+=1
        if userid is None:
            continue
        
        document={"userid":userid,"articles": [articleid]}
        a= monconn.loadFromTable({"userid":userid})
        #print a
    
        if not a:
         #   print "Hello"
            monconn.saveToTable(document)
        else:
            a[0]["articles"].append(articleid)
            monconn.saveToTable(a[0])
        
        
        
        
            
            
        
        
    
    
