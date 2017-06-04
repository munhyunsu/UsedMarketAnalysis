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
def get_city_mmdb(ip):
    global mmdb_reader
    try:
        response = mmdb_reader.city(ip)
        return response.city.name
    except geoip2.errors.AddressNotFoundError:
        return 'None'
# End of get_latlng_ip_mmdb



# Get lat, lng from IP2
def get_city_ip2(ip):
    global ip2_reader
    response = ip2_reader.get_all(ip)
    return response.city
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
    if len(sys.argv) < 2:
        print('We need 1 arguments')
        print('.py [SRC] [DES]')
        sys.exit()
    src_path = sys.argv[1]

    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)



    mdict = dict()
    idict = dict()
    for row in src_csv:
        mmdb_city = get_city_mmdb(row['start'])
        ip2_city = get_city_ip2(row['start'])

        mdict[mmdb_city] = mdict.get(mmdb_city, 0) + int(row['c24'])*4
        idict[ip2_city] = idict.get(ip2_city, 0) + int(row['c24'])*4

    print(mdict)
    print(idict)



# End of main()
##### ##### ===== 함수 선언 지역 끝 =====





if __name__ == '__main__':
    init()
    main()
    afterMain()
