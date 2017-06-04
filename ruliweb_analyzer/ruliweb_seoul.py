#!/usr/bin/python
# -*- coding: utf-8 -*-




##### ##### ===== 포함 지역 =====
# 인자
import sys
# CSV
import csv
import json
# Maxmind Database
import geoip2.database
# IP2Location Database
import IP2Location
import geopy
import pickle
import geopy.distance
# url
import urllib.request
import urllib.parse
import time
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
    mmdb_reader = geoip2.database.Reader('./GeoIP2-City.mmdb')
    
    # geopy_nomi set-up
    # city_latlng set-up
    global geopy_nomi
    global city_latlng
    geopy_nomi = geopy.geocoders.Nominatim()
    try:
        pkl_file = open('./city_latlng.pkl', 'rb')
        city_latlng = pickle.load(pkl_file)
        pkl_file.close()
    except:
        city_latlng = dict()

    # ip2_readet set-up
    global ip2_reader
    ip2_reader = IP2Location.IP2Location()
    ip2_reader.open('./IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE.BIN')
# End of Init



# After main
def afterMain():
    global city_latlng

    pkl_file = open('./city_latlng.pkl', 'wb')
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
def get_latlng_ruliweb(district, city):
    try:
        return city_latlng[(district, city)]
    except:
        location = google_maps_api(district, city)
        #print 'New: ', city, location.latitude, location.longitude
        city_latlng[(district, city)] = (location['lat'], location['lng'])
        return city_latlng[(district, city)]
#   print geopy_nomi.geocode(city.encode('utf-8'))


def google_maps_api(district, city):
    time.sleep(2)
    if district == city:
        city = ''
    if city in {'동', '서', '남', '북', '중'}:
        city = city + '구'
    request_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    request_url = request_url + urllib.parse.quote(district + ' ' + city)
    request_url = request_url + '&key=AIzaSyCz1vZgkgSVtF7Tr7IYAdjvCsnvqyacojw'
    response = urllib.request.urlopen(request_url)
    rjson = json.loads(response.read())
    try:
        return rjson['results'][0]['geometry']['location']
    except:
        print('Error' + district + city)
        afterMain()

# Get distance of latlngs
def get_distance_vincenty(latlng1, latlng2):
    return geopy.distance.vincenty(latlng1, latlng2).kilometers
# End of get_distance_vincenty


# Start of main()
def main():
    # 인자 파싱
    if len(sys.argv) < 3:
        print('We need 1 arguments')
        print('.py [SRC] [DES]')
        sys.exit()
    src_path = sys.argv[1]
    des_path = sys.argv[2]

    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    des_file = open(des_path, 'w')
    des_csv = csv.DictWriter(des_file, fieldnames = [
            'ruliweb', 'maxmind', 'ip2location'])
    des_csv.writeheader()

    seoul_latlng = (37.5653161,126.9745829)

    for row in src_csv:
        print(row)
        ruliweb_latlng = get_latlng_ruliweb(row['district'], row['city'])
        mmdb_latlng = get_latlng_mmdb(row['ipprefix'])
        ip2_latlng = get_latlng_ip2(row['ipprefix'])

        ruliweb_distance = get_distance_vincenty(seoul_latlng, ruliweb_latlng)
        maxmind_distance = get_distance_vincenty(seoul_latlng, mmdb_latlng)
        ip2location_distance = get_distance_vincenty(seoul_latlng, ip2_latlng)

        des_csv.writerow({'ruliweb': ruliweb_distance,
                          'maxmind': maxmind_distance,
                          'ip2location': ip2location_distance})
    # Calculate Distance
#   for (article_number, article_location, article_ip) in target_list:
#       city_latlng = get_latlng_city(article_location)
#       mmdb_latlng = get_latlng_mmdb(article_ip)
#       ip2_latlng = get_latlng_ip2(article_ip)
#
#       # distance of each latlng
#       maxmind_distance = get_distance_vincenty(city_latlng, mmdb_latlng)
#       ip2location_distance = get_distance_vincenty(city_latlng, ip2_latlng)
#
#       if(maxmind_distance > 500) or (ip2location_distance > 500):
#           print article_number, article_ip, city_latlng, mmdb_latlng, ip2_latlng, maxmind_distance, ip2location_distance
#
#       cur.execute('''INSERT OR IGNORE INTO distance (article_number, article_location, maxmind_distance, ip2location_distance) VALUES ( ?, ?, ?, ? )''', (article_number, article_location, maxmind_distance, ip2location_distance) )
#   conn.commit()


# End of main()
##### ##### ===== 함수 선언 지역 끝 =====





if __name__ == '__main__':
    init()
    main()
    afterMain()
