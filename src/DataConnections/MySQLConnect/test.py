
__author__="Harshit.Kashiv"

import MySQLdb

if __name__ == '__main__':
	print 'Hi'

	host="localhost"
	user="root"
	password="Km7Iv80l"
	database="cja_test_anand"
	unix_socket="/tmp/mysql.sock"

	db = MySQLdb.connect(host = host, user = user, passwd=password, db = database, unix_socket = unix_socket)
	cur = cursor = db.cursor(MySQLdb.cursors.DictCursor)

	#cmd = '''select * from check2 limit 1'''
	

	#cmd = '''insert into check2 values (1,2)'''
	cmd = '''delete from jobrec'''
	cur.execute(cmd)

	#for i in xrange(24, 40):
	#	cmd = '''insert into jobrec values (''' + str(i) +  ''', '1,2,3')'''

	params = []
	
	for i in [2,2,2]:
		#cmd = '''INSERT INTO jobrec (resid, jobs2bsent) VALUES (%s, %s) on duplicate key update resid = %s, jobs2bsent = %s, (resid, jobs2bsent)'''
		
		resid = i
		jobs2bsent = '1,2,3'
		params.append((resid, jobs2bsent))

	print params
	print cmd
	print resid
		
	try:
		cmd = '''INSERT IGNORE INTO jobrec (resid, jobs2bsent) VALUES (%s, %s)'''
		cur.executemany(cmd, params)
	except:
		db.rollback()
	else:
		db.commit()

