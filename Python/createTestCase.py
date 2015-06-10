import sqlite3

conn = sqlite3.connect('../Point_by_Point.db')
conn.text_factory = str

c = conn.cursor()

# Weights table
weights = {1:[1],2:[0.3,0.7],3:[0.2,0.4,0.4],4:[0.1,0.1,0.4,0.4],5:[0.05,0.05,0.1,0.4,0.4]}

# P1 Headers
p1Headers = ['P1ACE','P1NETPOINTWON','P1BREAKPOINTWON','P1FIRSTSRVWON','P1FIRSTSRVIN','P1DOUBLEFAULT','P1FORCEDERROR','P1SECONDSRVIN','P1WINNER','P1NETPOINT','P1BREAKPOINTMISSED','P1UNFERR','P1BREAKPOINT','P1SECONDSRVWON']
# P2 Headers
p2Headers = ['P2ACE','P2NETPOINTWON','P2BREAKPOINTWON','P2FIRSTSRVWON','P2FIRSTSRVIN','P2DOUBLEFAULT','P2FORCEDERROR','P2SECONDSRVIN','P2WINNER','P2NETPOINT','P2BREAKPOINTMISSED','P2UNFERR','P2BREAKPOINT','P2SECONDSRVWON']

headers = [p1Headers, p2Headers]



def createPlayerAvgData(player, tournament):
	sql = 'CREATE TABLE python_tmp_ply_avg_data AS SELECT  YEAR,AVG(ACE) AS ACE, AVG(NETPOINTWON) AS NETPOINTWON, AVG(BREAKPOINTWON) AS BREAKPOINTWON, AVG(FIRSTSRVWON) AS FIRSTSRVWON, AVG(FIRSTSRVIN) AS FIRSTSRVIN, AVG(DOUBLEFAULT) AS DOUBLEFAULT, AVG(FORCEDERROR) AS FORCEDERROR, AVG(SECONDSRVIN) AS SECONDSRVIN, AVG(WINNER) AS WINNER, AVG(NETPOINT) AS NETPOINT, AVG(BREAKPOINTMISSED) AS BREAKPOINTMISSED, AVG(UNFERR) AS UNFERR, AVG(BREAKPOINT) AS BREAKPOINT, AVG(SECONDSRVWON) AS SECONDSRVWON FROM (SELECT  YEAR, P1ACE AS ACE,P1NETPOINTWON AS NETPOINTWON,P1BREAKPOINTWON AS BREAKPOINTWON,P1FIRSTSRVWON AS FIRSTSRVWON,P1FIRSTSRVIN AS FIRSTSRVIN,P1DOUBLEFAULT AS DOUBLEFAULT,P1FORCEDERROR AS FORCEDERROR,P1SECONDSRVIN AS SECONDSRVIN,P1WINNER AS WINNER,P1NETPOINT AS NETPOINT,P1BREAKPOINTMISSED AS BREAKPOINTMISSED,P1UNFERR AS UNFERR,P1BREAKPOINT AS BREAKPOINT,P1SECONDSRVWON AS SECONDSRVWON FROM ALL_TOURNAMENTS_2011_2015 WHERE TOURNAMENT = ? AND PLAYER1 LIKE ? UNION ALL SELECT  YEAR,P2ACE AS ACE,P1NETPOINTWON AS NETPOINTWON,P2BREAKPOINTWON AS BREAKPOINTWON,P2FIRSTSRVWON AS FIRSTSRVWON,P2FIRSTSRVIN AS FIRSTSRVIN,P2DOUBLEFAULT AS DOUBLEFAULT,P2FORCEDERROR AS FORCEDERROR,P2SECONDSRVIN AS SECONDSRVIN,P2WINNER AS WINNER,P2NETPOINT AS NETPOINT,P2BREAKPOINTMISSED AS BREAKPOINTMISSED,P2UNFERR AS UNFERR,P2BREAKPOINT AS BREAKPOINT,P2SECONDSRVWON AS SECONDSRVWON FROM ALL_TOURNAMENTS_2011_2015 WHERE TOURNAMENT = ? AND PLAYER2 LIKE ?) GROUP BY YEAR ORDER BY YEAR;'
	print '\nCreating temp table:'
	print sql
	c.execute(sql, [(tournament), (player), (tournament), (player)])
	conn.commit()

def getWeightsTable(player, tournament):
	sql = 'SELECT count(*) FROM python_tmp_ply_avg_data;'
	print '\nCreating temp table:'
	print sql
	for row in c.execute(sql):
		return weights[row[0]]


def createPlayerAvgDataWeighted(player, tournament):
	createPlayerAvgData(player, tournament)
	w = getWeightsTable(player, tournament)

	sql = 'CREATE TABLE python_tmp_ply_avg_data_weighted AS SELECT * FROM python_tmp_ply_avg_data LIMIT 0'
	print '\nCreating temp table:'
	print sql
	c.execute(sql)
	conn.commit()

	sql = 'SELECT * FROM python_tmp_ply_avg_data'

	n = 0
	values = []
	for row in c.execute(sql):
		weightedRow = [float(i) * w[n] for i in row]
		weightedRow[0] = row[0]
		var_string = ', '.join('?' * len(weightedRow))
		values.append(weightedRow)
		n += 1
	sql = 'INSERT INTO python_tmp_ply_avg_data_weighted VALUES(' + var_string + ')'
	print 'Inserting data:'
	print sql
	c.executemany(sql, values)
	conn.commit()


def dropTmpTables():
	sql = 'DROP TABLE python_tmp_ply_avg_data;'
	print '\nDroping temp table:'
	print sql
	c.execute(sql)
	sql = 'DROP TABLE python_tmp_ply_avg_data_weighted;'
	print '\nDroping temp table:'
	print sql
	c.execute(sql)
	conn.commit()


def retrievePlayerData(player_name, player_n, tournament):
	global headers

	sql = 'SELECT SUM(ACE) AS ACE, 	SUM(NETPOINTWON) AS NETPOINTWON, 	SUM(BREAKPOINTWON) AS BREAKPOINTWON, 	SUM(FIRSTSRVWON) AS FIRSTSRVWON, 	SUM(FIRSTSRVIN) AS FIRSTSRVIN, 	SUM(DOUBLEFAULT) AS DOUBLEFAULT, 	SUM(FORCEDERROR) AS FORCEDERROR, 	SUM(SECONDSRVIN) AS SECONDSRVIN, 	SUM(WINNER) AS WINNER, 	SUM(NETPOINT) AS NETPOINT, 	SUM(BREAKPOINTMISSED) AS BREAKPOINTMISSED, 	SUM(UNFERR) AS UNFERR, 	SUM(BREAKPOINT) AS BREAKPOINT, 	SUM(SECONDSRVWON) AS SECONDSRVWON FROM python_tmp_ply_avg_data_weighted;'

	if player_n not in [1,2]:
		raise NameError('Not valid player number! Enter 1 or 2...')

	pHeaders = headers[player_n-1]

	createPlayerAvgDataWeighted(player_name, tournament)
	resultDict = {}
	
	for row in c.execute(sql):
		for i in range(len(row)):
			resultDict.update({pHeaders[i]:row[i]})
	dropTmpTables();

	return resultDict


def retrieveTrainingData():
	sql = "SELECT P1ACE,	P1BREAKPOINT,	P1BREAKPOINTMISSED,	P1BREAKPOINTWON,	P1DOUBLEFAULT,	P1FIRSTSRVIN,	P1FIRSTSRVWON,	P1FORCEDERROR,	P1NETPOINT,	P1NETPOINTWON,	P1SECONDSRVIN,	P1SECONDSRVWON,	P1UNFERR,	P1WINNER,	P2ACE,	P2BREAKPOINT,	P2BREAKPOINTMISSED,	P2BREAKPOINTWON,	P2DOUBLEFAULT,	P2FIRSTSRVIN,	P2FIRSTSRVWON,	P2FORCEDERROR,	P2NETPOINT,	P2NETPOINTWON,	P2SECONDSRVIN,	P2SECONDSRVWON,	P2UNFERR,	P2WINNER, SURF_CODE, CASE(WINNER) WHEN 1 THEN 'Player1' WHEN 2 THEN 'Player2' END AS WINNER FROM ALL_TOURNAMENTS_2011_2015 AS A INNER JOIN SURFACE_BY_TOURNAMENT AS B ON A.TOURNAMENT = B.TOURNAMENT WHERE WINNER IS NOT NULL"
	print '\nGenerating training data from query:'
	print sql

	samples = []
	classif = []

	for row in c.execute(sql):
		lRow = list(row)
		classif.append(lRow.pop(len(lRow)-1))
		samples.append(lRow)

	return samples, classif


def createTrainingInstance(player1_name, player2_name, tournament):
	result = []

	dictP1= retrievePlayerData(player1_name,1,tournament)
	dictP2= retrievePlayerData(player2_name,2,tournament)

	columns = sorted(dictP1.keys())
	for col in columns:
		result.append(int(round(dictP1[col])))

	columns = sorted(dictP2.keys())
	for col in columns:
		result.append(int(round(dictP2[col])))

	# Retrieve tournament surface code

	sql = "SELECT DISTINCT SURF_CODE FROM  SURFACE_BY_TOURNAMENT WHERE TOURNAMENT LIKE ?"

	for row in c.execute(sql, [(tournament)]):
		surfCode = row[0]

	result.append(surfCode)

	return result


def isValidPlayer(name):
	sql = "SELECT COUNT(PLAYER) FROM (SELECT distinct PLAYER1 AS PLAYER FROM ALL_TOURNAMENTS_2011_2015 WHERE PLAYER1 LIKE ? UNION SELECT distinct PLAYER2 AS PLAYER FROM ALL_TOURNAMENTS_2011_2015 WHERE PLAYER2 LIKE ?);"

	for row in c.execute(sql,[(name), (name)]):
		n = row[0]
		if n > 0:
			return True
		else:
			return False