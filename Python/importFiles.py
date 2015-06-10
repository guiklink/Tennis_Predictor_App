import sqlite3
import os
import csv
from decimal import Decimal

dir = './Data_Archive/ATP'

conn = sqlite3.connect('ATP.db')
conn.text_factory = str

c = conn.cursor()

STR_TYPE = 'VARCHAR(255)'
INT_TYPE = 'INT'
FLOAT_TYPE = 'DOUBLE'

INVALID_CHARS_IN_COLUMN_NAME = ['?','#']

SQL_RESERVED_WORDS = {'SET':'SET_',' ':'_','-':'_','?':'','#':'','+':'PLUS','&':'_AND_','.':'_'}

def removedReservedWordsSQL(str):
	global SQL_RESERVED_WORDS

	s = str
	for word in SQL_RESERVED_WORDS.keys():
		s = s.replace(word,SQL_RESERVED_WORDS[word])
	return s


def retrieveFiles(path):
	results = []
	results += [each for each in os.listdir(path) if each.endswith('.csv')]
	return results


def getDataType(val):
	try:
		float(val)
	except Exception, e:
		return STR_TYPE
	else:
		if Decimal(val) % 1 == 0:
			return INT_TYPE
		else:
			return FLOAT_TYPE


def properColumnName(str):
	sqlFormat = str.upper()
	sqlFormat = removedReservedWordsSQL(sqlFormat)
	return sqlFormat


def getColumnTypes(path, file):
	op = open(path + '/' + file, 'rb')
	dr = csv.DictReader(op)

	columns = dr.fieldnames
	resulDict = dict.fromkeys(map(properColumnName,columns))

	# Find out the type for each column
	for row in dr:
		for column in columns:
			if resulDict[properColumnName(column)] == STR_TYPE:
				pass	# Do nothing
			else:
				cType = getDataType(row[column])

				if cType == STR_TYPE:
					resulDict.update({properColumnName(column):cType})

				elif cType == FLOAT_TYPE:
					if resulDict[properColumnName(column)] == INT_TYPE or resulDict[properColumnName(column)] == None:
						resulDict.update({properColumnName(column):cType})

				elif cType == INT_TYPE:
					if resulDict[properColumnName(column)] == None:
						resulDict.update({properColumnName(column):cType})

	return resulDict


def getQuery_createTable(path, file):
	sql = 'CREATE TABLE ' + 'RAW_' + properColumnName(file[0:-4]) + ' ('

	cDict = getColumnTypes(path,file)

	for col in cDict.keys():
		sql += col + ' ' + cDict[col] + ', '

	sql = sql[0:-2] + ')'
	
	return sql


def importQuery_inserInto(path, file):
	op = open(path + '/' + file, 'rb')
	dr = csv.DictReader(op)

	columns = dr.fieldnames
	valuesList = []
	values = ()

	# Find out the type for each column
	for row in dr:
		for column in columns:
			values += (str(row[column]),)
		valuesList.append(values)
		values = ()

	sql = 'INSERT INTO ' + 'RAW_' + properColumnName(file[0:-4]) + ' (' + ', '.join(map(properColumnName,columns)) + ') VALUES ('
	for i in range(len(columns)):
	 	sql += '?,'

	sql = sql[0:-1] + ')'

	# print '\n\n####### '
	# print valuesList 

	return sql, valuesList


def importTable(path, file):
	global c, conn

	createTableSQL = getQuery_createTable(path, file)

	print '\nCreating Table: '
	print createTableSQL
	c.execute(createTableSQL)

	insertSQL, valuesList = importQuery_inserInto(path, file)

	print '\nInserting Data: '
	print insertSQL
	c.executemany(insertSQL, valuesList)
	conn.commit()


def getListOfTablesInDB():
	global c

	sql = 'SELECT name FROM sqlite_master WHERE type = "table"'

	result = []
	for row in c.execute(sql):
		result.append(str(row).replace(')','').replace('(','').replace('u\'','').replace(',','').replace("'",""));
	return result 


def main():
	global dir

	files = retrieveFiles(dir)
	tablesInDB = getListOfTablesInDB();

	for f in files:
		if 'RAW_' + properColumnName(f[0:-4]) not in tablesInDB:
			try:
				importTable(dir,f)
			except Exception, e:
				print '\n\n>>>> ERROR Importing: ' + str(f) + ': '
				print '>>>>>> ' + str(e) + '\n'
			else:
				print '\n\n (*) File Imported: ' + str(f) + '\n\n'
		else:
			print '\n\n (!!!) A file with this name was already imported: ' + str(f) + '\n       For safety it will not be imported again. Rename the file and try again.\n\n'
		

if __name__ == '__main__':
	main()
