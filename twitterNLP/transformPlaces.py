import sys, json, re
sys.path.append('./database/DAO')
from DatabaseManager import DatabaseManager


def main():

	print "Reading minID"
	fp = open('ids.txt', 'r')
	for line in fp:
		ids = line.strip().split(",")
		minID = ids[0]
		maxID = ids[1]
	fp.close()

	print "minID: ", minID

	dbm = DatabaseManager()

	print "running query..."

	places = dbm.runQuery("SELECT id, bounding_box FROM Places \
						   WHERE lat_1 IS NULL AND id > {0} AND id < {1}".format(minID, maxID))

	print "query done!"
	cont = 0.0;

	for row in places:
		try:
			idPlace = row[0]
			bounding_box = row[1]
			tmp = re.sub(r'u\'','\'', bounding_box)
			tmp = re.sub(r'\'','"', tmp)
			obj = json.loads(tmp)
			box_coords = obj['coordinates'][0]
			
			lat_1 = box_coords[0][1]
			long_1 = box_coords[0][0]
			lat_2 = box_coords[1][1]
			long_2 = box_coords[1][0]
			lat_3 = box_coords[2][1]
			long_3 = box_coords[2][0]
			lat_4 = box_coords[3][1]
			long_4 = box_coords[3][0]

			query = u"""UPDATE Places SET lat_1={0}, long_1={1}, lat_2={2}, long_2={3},lat_3={4}, long_3={5}, lat_4={6}, long_4={7} WHERE id = {8}""".format(lat_1, long_1, lat_2, long_2, lat_3, long_3, lat_4, long_4, idPlace)
			print "%i" % (cont)
			dbm.runCommit(query)

		except Exception as e:
			print "error with id=", row[0]
			print e
		cont += 1

if __name__ == '__main__':
	main()
