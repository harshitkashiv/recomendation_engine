
__author__="Harshit.Kashiv"

__date__ ="$Mar10, 2015 16:00 PM$"

'''
This module provides functions for connecting to Mongodb and reading and writing data to it
'''

#Include the root directory in the path
import sys
sys.path.append('./../../')

import pymongo
#from pymongo import MongoClient

class MongoConnect():
	def __init__(self, table,database = 'capi_logs', host = 'localhost', port = 27017):
		#Used all times except when first table is created

		#Make a mongodb connection
		self.connection = pymongo.Connection(host, port)

		#self.connection = pymongo.mongo_client.MongoClient(host,port) #Works with pymongo2.4+
		self.table = self.connection[database][table] #test_cja is the db name
	

	def doIndexing(self, table, indexFields, database = 'capi_logs', host = 'localhost', port = 27017, ukey = False):
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

		

if __name__ == '__main__':
	print 'Mongo connect module:'
	
	print 'Hi'

	#db.contacts.save({'name':'anand','email':'anandmishraiitk@gmail.com'})
	
	tableName = 'contacts'
	indexFields = [('name',pymongo.ASCENDING)]
	#monconn = MongoConnect(tableName, indexFields)
	monconn = MongoConnect(tableName)
	monconn.doIndexing(tableName, indexFields)	

	#document = {'name':'anand','email':'anandmishraiitk@gmail.com'}
	document = {'name':'julie','email':'julie@gmail.com'}
	monconn.saveToTable(document)

	myCondition= {'name':'julie'}
	s = monconn.loadFromTable(myCondition)
	#print s
	#print len(s)

	for i in xrange(1,10):
		document = {'id':i,'name':'julie','email':'julie@gmail.com'}
		monconn.saveToTable(document)

	print monconn.subsetTable(tableName)
	
	myCondition = {'id': { '$mod': [ 4, 0 ] } }
	print monconn.loadFromTable(myCondition)
