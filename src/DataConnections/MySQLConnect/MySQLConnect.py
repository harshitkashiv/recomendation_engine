
__author__="Harshit.Kashiv"

__date__ ="Mar10, 2015 11:18 AM$"

'''
This module provides functions for connecting to MySQL database and fetching data from it
Given connection parameters one can make a MySQLConnect object and query the object
5/22/13 -- Added autocommit and insert functionality
'''

#Include the root directory in the path
import sys
sys.path.append('./../../')

import MySQLdb
import traceback


class MySQLConnect():
	def __init__(self, database, host = "localhost", user = "root", password = "abcd@1234", unix_socket = "/tmp/mysql.sock", port = 3306):
		self.db = MySQLdb.connect(host = host, user = user, passwd=password, db = database, unix_socket = unix_socket, port = port)
#		self.db = MySQLdb.connect(host = host, user = user, passwd=password, db = database)
	
		#Set the autocommit flag to true, not to worry about commit when writing
		self.db.autocommit(True)
	
		self.cur = cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

	def query(self, query, type = 'select', writeVals = ()):
		if type == 'select':
			self.cur.execute(query)
			return self.cur.fetchall()
		else:
			return self.cur

	def getCursor(self):
			return self.cur

	def saveToTable(self, query, writeVals = ()):
		try:
			self.cur.execute(query, writeVals)

			#self.cur.execute(query)
			#writeVals = ("242", "1,2,3")
			#self.cur.execute('''insert into jobrec (resid, jobs2bsent) values (%s, %s)''', ("242", "1,2,3"))
			self.db.commit()
			#print '0'
			return 0

		except:
			traceback.print_exc()
			print '-1'
			#self.db.rollback()
			return -1

	def close(self):
		self.cur.close()
		self.db.close()


if __name__ == '__main__':
	print 'MySQL connect module:'
	
	host="localhost"
	user="root"
	password="xxxxx"
	database="abcd"
	unix_socket="/tmp/mysql.sock"

	db = MySQLConnect(database, host, user, password, unix_socket)
	cmd = '''select * from CJA_UserDetails limit 1'''
	print db.query(cmd)


	#cmd = '''insert into check2 values (122,2)'''
	
	cmd = '''insert into jobrec values (%s, %s)'''
	writeVals = ("242", "1,2,3")

	print db.saveToTable(cmd, writeVals = writeVals)