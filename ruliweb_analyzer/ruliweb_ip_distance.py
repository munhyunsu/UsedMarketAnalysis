#!/usr/bin/python
# -*- coding: utf-8 -*-




##### ##### ===== 포함 지역 =====
# 인자
import sys
# Database
import sqlite3
# Maxmind Database
import geoip2.database
# IP2Location Database
import IP2Location
import geopy
import pickle
import geopy.distance
##### ##### ===== 포함 지역 끝 =====





##### ##### ===== 함수 선언 지역 =====
# Init
mmdb_reader = None
geopy_nomi = None
city_latlng = None
ip2_reader = None
def init():
	# mmdb_reader set-up
	global mmdb_reader
	mmdb_reader = geoip2.database.Reader('./tlib/GeoIP2-City.mmdb')
	
	# geopy_nomi set-up
	# city_latlng set-up
	global geopy_nomi
	global city_latlng
	geopy_nomi = geopy.geocoders.Nominatim()
	try:
		pkl_file = open('./tlib/city_latlng.pkl', 'rb')
		city_latlng = pickle.load(pkl_file)
		pkl_file.close()
	except:
		city_latlng = dict()

	# ip2_readet set-up
	global ip2_reader
	ip2_reader = IP2Location.IP2Location()
	ip2_reader.open('./tlib/IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE.BIN')
# End of Init



# After main
def afterMain():
	global city_latlng

	pkl_file = open('./tlib/city_latlng.pkl', 'wb')
	pickle.dump(city_latlng, pkl_file)
	pkl_file.close()

# End of after_main()



# Get lat, lng from mmdb
def get_latlng_mmdb(ip):
	global mmdb_reader
	try:
		response = mmdb_reader.city(ip)
		return (response.location.latitude, response.location.longitude)
	except geoip2.errors.AddressNotFoundError:
		response = (37.5985, 126.9783)
		return response
# End of get_latlng_ip_mmdb



# Get lat, lng from IP2
def get_latlng_ip2(ip):
	global ip2_reader
	response = ip2_reader.get_all(ip)
	return (response.latitude, response.longitude)
# End of get_latlng_ip_ip2



# Get lat, lng from city name
def get_latlng_city(city):
	try:
		return city_latlng[city]
	except KeyError:
		location = geopy_nomi.geocode(city)
		#print 'New: ', city, location.latitude, location.longitude
		city_latlng[city] = (location.latitude, location.longitude)
		return city_latlng[city]
#	print geopy_nomi.geocode(city.encode('utf-8'))



# Get distance of latlngs
def get_distance_vincenty(latlng1, latlng2):
	return geopy.distance.vincenty(latlng1, latlng2).kilometers
# End of get_distance_vincenty


# Start of to_cidr()
# Convert ip to CIDR
def to_cidr(ip_address, block):
	"""
	Convert IP Address to CIDR string
	"""
	list_address = ip_address.split('.')
	
	bi_address = list()
	for address in list_address:
		bi_address.append('{:08b}'.format(int(address)))	

	bi_address = ''.join(bi_address)
	bi_address = int(bi_address, 2)

	# 4294967295
	# 4294967294
	# 4294967292
	# ...
	count = block
	mask = 4294967295
	bi_pow = 1
	while count != 32:
		mask = mask - bi_pow
		bi_pow = bi_pow * 2
		count = count + 1

	#str_mask = str('{:032b}'.format(mask))

	#for i in range(0, 4):
	#	print str_mask[i*8:(i+1)*8]
	result_address = bi_address & mask
	result_address = '{:032b}'.format(result_address)
	#result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2)) + '/' + str(block)
	result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2))

	return result
# End of to_cidr()



# Start of main()
def main():
	# 인자 파싱
	if len(sys.argv) < 2:
		print 'We need 1 arguments'
		print '.py [DB]'
		sys.exit()
	db_path = sys.argv[1]

	# Database Connector
	conn = sqlite3.connect(db_path)
	# Database Cursor
	cur = conn.cursor()

	# Create Table
	#cur.execute('DROP TABLE IF EXISTS geodb')
	#conn.commit()
	cur.executescript('''
		CREATE TABLE IF NOT EXISTS geodb (
			ip_address TEXT PRIMARY KEY NOT NULL UNIQUE,
			location TEXT NOT NULL);
		'''
	)
	conn.commit()

	# Create Table
	#cur.execute('DROP TABLE IF EXISTS distance')
	#conn.commit()
	cur.executescript('''
		CREATE TABLE IF NOT EXISTS distance (
			article_number INTEGER PRIMARY KEY NOT NULL UNIQUE,
			article_location TEXT NOT NULL,
			maxmind_distance REAL NOT NULL,
			ip2location_distance REAL NOT NULL);
		'''
	)
	conn.commit()

	# Read article_location
	cur.execute('''SELECT article_location, article_ip FROM ruliweb''')
	target_list = cur.fetchall()

	# Make GeoDB
	for (article_location, article_ip) in target_list:
		ip_address = to_cidr(article_ip, 26)
		cur.execute('''INSERT OR IGNORE INTO geodb (ip_address, location) VALUES ( ?, ? )''', (ip_address, article_location) )
		ip_address = to_cidr(article_ip, 25)
		cur.execute('''INSERT OR IGNORE INTO geodb (ip_address, location) VALUES ( ?, ? )''', (ip_address, article_location) )
		ip_address = to_cidr(article_ip, 24)
		cur.execute('''INSERT OR IGNORE INTO geodb (ip_address, location) VALUES ( ?, ? )''', (ip_address, article_location) )
	conn.commit()

	# Read article infomation
	cur.execute('''SELECT article_number, article_location, article_ip FROM ruliweb''')
	target_list = cur.fetchall()

	# Calculate Distance
	for (article_number, article_location, article_ip) in target_list:
		city_latlng = get_latlng_city(article_location)
		mmdb_latlng = get_latlng_mmdb(article_ip)
		ip2_latlng = get_latlng_ip2(article_ip)

		# distance of each latlng
		maxmind_distance = get_distance_vincenty(city_latlng, mmdb_latlng)
		ip2location_distance = get_distance_vincenty(city_latlng, ip2_latlng)

		if(maxmind_distance > 500) or (ip2location_distance > 500):
			print article_number, article_ip, city_latlng, mmdb_latlng, ip2_latlng, maxmind_distance, ip2location_distance

		cur.execute('''INSERT OR IGNORE INTO distance (article_number, article_location, maxmind_distance, ip2location_distance) VALUES ( ?, ?, ?, ? )''', (article_number, article_location, maxmind_distance, ip2location_distance) )
	conn.commit()


# End of main()
##### ##### ===== 함수 선언 지역 끝 =====





if __name__ == '__main__':
	init()
	main()
	afterMain()
