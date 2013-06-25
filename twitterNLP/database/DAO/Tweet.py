from User import User
from Place import Place

class Tweet:

	def __init__(self, databaseMngr = None):
		self.tweetID = "NULL"
		self.from_user = None #User Object
		self.tweet = ""
		self.created_at = ""
		self.place = None #Place Object
		self.source = ""
		self.favorite_count = 0
		self.coordinates = ""
		self.geo = ""
		self.lang = ""
		self.filter_level = ""
		self.in_reply_to_status_id_str = ""
		self.dbm = databaseMngr

	def set(self, tweetID = "NULL", from_user = None, tweet = "", created_at = "", place = None, source = "", favorite_count = 0, coordinates = "", geo = "", lang = "", filter_level = "", in_reply_to_status_id_str = ""):
		self.tweetID = tweetID
		self.from_user = from_user
		self.tweet = tweet
		self.created_at = created_at
		self.place = place
		self.source = source
		self.favorite_count = favorite_count
		self.coordinates = coordinates
		self.geo = geo
		self.lang = lang
		self.filter_level = filter_level
		self.in_reply_to_status_id_str = in_reply_to_status_id_str

	def save(self):
		"""Inserta un nuevo Tweet en la base de datos"""
		if self.dbm:

			if isinstance(self.place, Place):
				placeId = self.place.id2
			else:
				placeId = self.place

			query = u"""INSERT INTO Tweets(from_user_id, tweet, created_at, placeId, source, favorite_count, coordinates,
										  geo, lang, filter_level, in_reply_to_status_id_str, date_created)
					   VALUES ({1},\"{2}\",\"{3}\",\"{4}\",\"{5}\",{6},\"{7}\",\"{8}\",\"{9}\",\"{10}\",\"{11}\", STR_TO_DATE(\"{3}\", '%a %b %d %H:%i:%s +0000 %Y'))
					  """.format(self.tweetID, self.from_user.idUser if self.from_user is not None else 0, self.tweet, 
							   self.created_at, placeId, self.source, 
							   self.favorite_count, self.coordinates, self.geo, self.lang, self.filter_level, 
							   self.in_reply_to_status_id_str)
			return self.dbm.runCommit(query)
		else:
			raise Exception("No dbm declared")

	@staticmethod
	def searchTweetById(dbm, tweetID):
		"""Regresa un objeto Tweet para la id buscada"""
		tweetRes = Tweet(dbm)
		if dbm is not None:
			res = dbm.runQuery("SELECT tweetID, from_user_id, tweet, created_at, placeId, source, favorite_count, coordinates, userId, geo, lang, filter_level, in_reply_to_status_id_str FROM Tweets WHERE tweetID={}".format(tweetID))
			try:
				if res is not None:
					row = res[0]
					tweetRes.set(tweetID = row[0], from_user = User.searchUserById(dbm, row[1]), tweet = row[2], created_at = row[3],
								 place = Place.searchPlaceById(dbm, row[4]), source = row[5], favorite_count = row[6], coordinates = row[7], 
							 	 geo = row[9], lang = row[10], filter_level = row[11], in_reply_to_status_id_str = row[12])
			except:
				pass
			return tweetRes
		else:
			raise Exception("No DBM declared")

	@staticmethod
	def getAllTweets(dbm):
		"""Regresa una lista de objetos Tweet con todos los elementos de la tabla"""
		allTweets = []
		if dbm is not None:
			res = dbm.runQuery("SELECT tweetID, from_user_id, tweet, created_at, placeId, source, favorite_count, coordinates, userId, \
									   geo, lang, filter_level, in_reply_to_status_id_str FROM Tweets")
			for row in res:
				tweetRes = Tweet()
				tweetRes.set(tweetID = row[0], from_user = User.searchUserById(dbm, row[1]), tweet = row[2], created_at = row[3],
							 place = Place.searchPlaceById(dbm, row[4]), source = row[5], favorite_count = row[6], coordinates = row[7], 
						 	 geo = row[9], lang = row[10], filter_level = row[11], in_reply_to_status_id_str = row[12])
				tweetRes.dbm = dbm
				allTweets.append(tweetRes)
			return allTweets
		else:
			raise Exception("No DBM declared")

	@staticmethod
	def findTweetsWithoutSentiment(dbm):
		"""Regresa una lista de objetos Tweet que no han sido procesados por sentimiento"""
		nonSentiment = []
		if dbm is not None:
			res = dbm.runQuery("SELECT Tweets.tweetID, tweet FROM Tweets left join Sentiment on Tweets.tweetID = Sentiment.tweetID WHERE Sentiment.tweetID is null")

			for row in res:
				t = Tweet()
				t.tweetID = row[0]
				t.tweet = row[1]
				nonSentiment.append(t)
			return nonSentiment
		else:
			raise Exception("No DBM declared")

	@staticmethod
	def findTweetsFromLastMinutes(dbm, minutes=30):
		"""Regresa una lista de objetos Tweet que fueron agregados en los ultimos minutos"""
		tweets = []
		if dbm is not None:
			res = dbm.runQuery("SELECT tweetID, tweet FROM Tweets WHERE DATE_SUB(NOW(), INTERVAL %i MINUTE) <= date_created" % minutes)

			for row in res:
				t = Tweet()
				t.tweetId = row[0]
				t.tweet = row[1]
				tweets.append(t)
			return tweets
		else:
			raise Exception("No DBM declared")
