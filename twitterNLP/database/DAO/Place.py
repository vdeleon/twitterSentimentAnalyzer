class Place:

	def __init__(self, databaseMngr = None):
		self.idPlace = "NULL"
		self.full_name = ""
		self.url = ""
		self.country = ""
		self.place_type = ""
		self.bounding_box = ""
		self.lat_1 = ""
		self.long_1 = ""
		self.lat_2 = ""
		self.long_2 = ""
		self.lat_3 = ""
		self.long_3 = ""
		self.lat_4 = ""
		self.long_4 = ""
		self.country_code = ""
		self.attributes = ""
		self.name = ""
		self.id2 = ""
		self.dbm = databaseMngr

	def set(self, idPlace = "NULL", full_name = "", url = "", country = "", place_type = "", bounding_box = "", lat_1 = "", long_1 = "", lat_2 = "", long_2 = "", lat_3 = "", long_3 = "", lat_4 = "", long_4 = "", country_code = "", attributes = "", name = "", id2 = ""):
		"""Establece los campos del objeto Place"""
		self.idPlace = idPlace
		self.full_name = full_name
		self.url = url
		self.country = country
		self.place_type = place_type
		self.bounding_box = bounding_box
		self.lat_1 = lat_1
		self.long_1 = long_1
		self.lat_2 = lat_2
		self.long_2 = long_2
		self.lat_3 = lat_3
		self.long_3 = long_3
		self.lat_4 = lat_4
		self.long_4 = long_4
		self.country_code = country_code
		self.attributes = attributes
		self.name = name
		self.id2 = id2


	def saveOrUpdate(self):
		"""Actualiza o inserta un nuevo Place en la base de datos"""
		if self.dbm:
			query = u""" INSERT INTO Places(id, full_name, url, country, place_type, bounding_box, country_code, attributes, name, id2, lat_1, long_1, lat_2, long_2, lat_3, long_3, lat_4, long_4) 
						VALUES ({0},\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\",\"{7}\",\"{8}\",\"{9}\", {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17})
						ON DUPLICATE KEY UPDATE id=VALUES(id), full_name=VALUES(full_name), url=VALUES(url), country=VALUES(country), 
												place_type=VALUES(place_type), bounding_box=VALUES(bounding_box), country_code=VALUES(country_code),
												attributes=VALUES(attributes), name=VALUES(name), id2=VALUES(id2),
												lat_1=VALUES(lat_1), long_1=VALUES(long_1), lat_2=VALUES(lat_2), long_2=VALUES(long_2),
											    lat_3=VALUES(lat_3), long_3=VALUES(long_3), lat_4=VALUES(lat_4), long_4=VALUES(long_4)
					""".format(self.idPlace, self.full_name, self.url, self.country, self.place_type, self.bounding_box, self.country_code, self.attributes, self.name, self.id2, self.lat_1, self.long_1, self.lat_2, self.long_2, self.lat_3, self.long_3, self.lat_4, self.long_4)
			self.dbm.runCommit(query)
		else:
			raise Exception("No DBM declared")

	@staticmethod
	def searchPlaceById(dbm, idPlace):
		"""Regresa un objeto Place para la id buscada"""
		placeRes = Place()
		if dbm is not None:
			res = dbm.runQuery("SELECT id, full_name, url, country, place_type, bounding_box, country_code, attributes, name, id2, \
								lat_1, long_1, lat_2, long_2, lat_3, long_3, lat_4, long_4 FROM Places WHERE id = {}".format(idPlace))
			if res is not None:
				row = res[0]
				placeRes.set(idPlace = row[0], full_name = row[1], url = row[2], country = row[3], place_type = row[4], bounding_box = row[5],
							 country_code = row[6], attributes = row[7], name = row[8], id2 = row[9], lat_1 = row[10], long_1 = row[11],
							 lat_2 = row[12], long_2 = row[13], lat_3 = row[14], long_3 = row[15], lat_4 = row[16], long_4 = row[17])
				return placeRes
		else:
			raise Exception("No DBM declared")
	
	@staticmethod
	def searchPlaceById2(dbm, id2):
		"""Regresa un objeto Place para la id2 buscada"""
		placeRes = Place(dbm)
		if dbm is not None:
			res = dbm.runQuery("SELECT id, full_name, url, country, place_type, bounding_box, country_code, attributes, name, id2, \
							    lat_1, long_1, lat_2, long_2, lat_3, long_3, lat_4, long_4 FROM Places WHERE id2 = {}".format(id2))
			try:
				if res is not None:
					row = res[0]
					placeRes.set(idPlace = row[0], full_name = row[1], url = row[2], country = row[3], place_type = row[4], bounding_box = row[5],
								 country_code = row[6], attributes = row[7], name = row[8], id2 = row[9], lat_1 = row[10], long_1 = row[11],
								 lat_2 = row[12], long_2 = row[13], lat_3 = row[14], long_3 = row[15], lat_4 = row[16], long_4 = row[17])
			except:
				pass
			return placeRes
		else:
			raise Exception("No DBM declared")


	@staticmethod
	def getAllPlaces(dbm):
		"""Regresa una lista de objetos Places con todos los elementos de la tabla"""
		allPlaces = []
		if dbm is not None:
			res = dbm.runQuery("SELECT id, full_name, url, country, place_type, bounding_box, country_code, attributes, name, id2, \
								lat_1, long_1, lat_2, long_2, lat_3, long_3, lat_4, long_4 FROM Places")
			for row in res:
				placeRes = Place()
				placeRes.set(idPlace = row[0], full_name = row[1], url = row[2], country = row[3], place_type = row[4], bounding_box = row[5],
							 country_code = row[6], attributes = row[7], name = row[8], id2 = row[9], lat_1 = row[10], long_1 = row[11],
						     lat_2 = row[12], long_2 = row[13], lat_3 = row[14], long_3 = row[15], lat_4 = row[16], long_4 = row[17])
				placeRes.dbm = dbm
				allPlaces.append(placeRes)
			return allPlaces
		else:
			raise Exception("No DBM declared")


	def __str__(self):
		return "Place<(%i)>".format(self.idPlace)