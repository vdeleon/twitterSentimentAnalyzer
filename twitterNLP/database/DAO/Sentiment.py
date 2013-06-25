from Tweet import Tweet

class Sentiment:

	def __init__(self, databaseMngr = None):
		self.tweet = None #Tweet Object
		self.sentiment = 0
		self.dbm = databaseMngr

	def set(self, tweet = None, sentiment = 0):
		self.tweet = tweet
		self.sentiment = sentiment

	def saveOrUpdate(self):
		if self.dbm is not None:
			query = """INSERT INTO Sentiment(tweetID, sentiment)
					   VALUES ({0},{1})
					   ON DUPLICATE KEY UPDATE sentiment = VALUES(sentiment)
					""".format(self.tweet.tweetID, self.sentiment)
			self.dbm.runCommit(query)
		else:
			raise Exception("No dbm declared")

	@staticmethod
	def searchSentimentByTweet(dbm, tweet):
		sentimentRes = Sentiment(dbm)
		if dbm is not None:
			res = dbm.runQuery("SELECT tweetID, sentiment FROM Sentiment WHERE tweetID = {0}".format(tweet.tweetID))
			try:	
				if res is not None:
					row = res[0]
					sentimentRes.set(Tweet.searchTweetById(dbm, row[0]), row[1])
			except:
				pass
			return sentimentRes
		else:
			raise Exception("No dbm declared")

	@staticmethod
	def getAllSentiments(dbm):
		allSentiments = []
		if dbm is not None:
			res = dbm.runQuery("SELECT tweetID, sentiment FROM Sentiment")
			for row in res:
				sentimentRes = Sentiment()
				tweet = Tweet.searchTweetById(dbm, row[0])
				sentimentRes.set(tweet, row[1])
				sentimentRes.dbm = dbm
				allSentiments.append(sentimentRes)
			return allSentiments
		else:
			raise Exception("No dbm declared")


	def __str__(self):
		return "Sentiment<(%i)> = %i".format(self.tweet.tweetID, self.sentiment)
