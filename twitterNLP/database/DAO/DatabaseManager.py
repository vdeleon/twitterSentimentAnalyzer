import MySQLdb
class DatabaseManager:
	def __init__(self):
		self.__err = ""
		self.isConnectionAlive = False
		self.db = None
		self.__query = ""

	def getConnection(self):
		try:
			if not self.isConnectionAlive:
				self.db = MySQLdb.connect(host="tweetsentimentvisualizerdb.cmbn4bw1jt6o.us-west-2.rds.amazonaws.com", user="vrmpx", passwd="tweetsdexe3575", db="tweetsDB")
				self.isConnectionAlive = True	
			return self.db
		except Exception, e:
			self.__err = e.message
			return None
		
	def getError(self):
		return self.__err

	def runQuery(self, query):
		"""Ejecuta la query deseada y devuelve una lista de resultados"""	
		try:
			self.__query = query
			cursor = self.getConnection().cursor()
			cursor.execute(query)
			return cursor.fetchall()
		except:
			return None

	def runCommit(self, query):
		"""Ejecuta la query deseada con commit"""
		try:
			self.__query = query
			cursor = self.getConnection().cursor()
			cursor.execute(query)
			self.db.commit()
			return True
		except Exception, e:
			print "Query: " + self.__query
			# print "ERR: " + e.message
			self.__err = e.message
			self.db.rollback()
			return False

	def __del__(self):
		if self.db:
			self.db.close()
		self.isConnectionAlive = None

