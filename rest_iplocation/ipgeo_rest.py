#!/usr/bin/env python
# -*- coding: utf8 -*-
# for arguments
import cgi
import cgitb
import sys

import sqlite3
import pickle
import os
import asyncio
import re
import json


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
        #       print str_mask[i*8:(i+1)*8]
        result_address = bi_address & mask
        result_address = '{:032b}'.format(result_address)
        result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2)) + '/' + str(block)

        return result

conn = sqlite3.connect('ruliweb_analysis.sqlite')
cur = conn.cursor()
scity = None
sip = None
scidrip = None
city_latlng = None
slat = None
slng = None
def find_luhadb(address):
    global conn
    global cur
    global city_latlng
    global scity
    global sip
    global scidrip
    global slat
    global slng

    try:
        pkl_file = open('./city_latlng.pkl', 'rb')
        city_latlng = pickle.load(pkl_file)
        pkl_file.close()
        if city_latlng is None:
            city_latlng = dict()
    except:
        city_latlng = dict()

    block = 32
    while block > 0:
        cidr_ip = to_cidr(address, block)
        ip_address = cidr_ip.split('/')[0]
        cur.execute('SELECT location FROM geodb WHERE ip_address LIKE "' + str(ip_address) + '"')
        city = cur.fetchone()
#       print ip_address, city
        if city is not None:
            return city[0]
        block = block - 1


@asyncio.coroutine
def ipgeo_rest(reader, writer):
    try:
        # 1. 요청 메시지 확인
        receive_data = yield from asyncio.wait_for(reader.read(1500), \
            timeout = 10.0) # 요청을 읽기
        receive_data = receive_data.decode()
        print(receive_data)
        # 1-1. HTTP 헤더를 제거하고 요청과 자원만 파싱
        receive_method = (receive_data.split('\r\n')[0]).split(' ')[0]

        # curl -X GET 'http://localhost:8800/login/dnlab/6292'
        if receive_method == 'GET':
            receive_path = (receive_data.split('\r\n')[0]).split(' ')[1]

            receive_do = receive_path.split('/')[1]
            city = find_luhadb(receive_do)

            if city is not None:
                # 2-4-1. 로그인이 성공했을 경우 처리
                send_data = 'HTTP/1.1 200 OK\r\n'
                send_data = send_data + 'Content-Type: application/json\r\n'
                send_data = send_data + '\r\n'
                send_data = send_data + '{"City": "' + city + '"}\r\n'
            else:
                # 2-4-2. 로그인이 실패했을 경우 처리
                send_data = 'HTTP/1.1 200 Not Found\r\n'
                send_data = send_data + 'Content-Type: application/json\r\n'
                send_data = send_data + '\r\n'
                send_data = send_data + '{"City": "Unknown"}\r\n'
            writer.write(send_data.encode())
            yield from asyncio.wait_for(writer.drain(), \
                    timeout = 10.0)
        writer.close()
    except Exception as err:
        # 소켓 종료
        print('Exception!', err)
        writer.close()



def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(ipgeo_rest, '', 8080, loop=loop)
    server = loop.run_until_complete(coro)

    # 5. Ctrl+C를 누를 때까지 서버 동작
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        # 6. Ctrl+C가 눌리면 서버 종료
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # 6-1. 서버가 종료될 때 아직 서비스중인 클라이언트가 있을 수 있음
    # 6-2. 서비스받는 클라이언트가 존재하면 서비스 마무리 후 종료
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
