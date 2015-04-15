# -*- coding: utf-8 -*-  

import re
import datetime
import urllib2
import json

#data  = "1010140002100.29Eb9010091000101.2Eb901007100001198Eb901010140002100.29Eb901010140002100.29Eb9010091000101.0Eb901007100001195Eb901010140002100.29Eb901010140002100.29Eb9010091000101.0Eb901007100001222Eb901010140002100.29Eb901010140002100.29Eb9010091000101.4Eb901007100001226Eb901010140002100.29Eb901010140002100.29Eb9010091000101.2Eb901007100001140Eb901010140002100.29Eb901010140002100.29Eb9010091000101.2Eb901007100001239Eb901010140002100.29Eb901010140002100.29Eb9010091000100.8Eb901007100001204Eb901010140002100.29Eb901010140002100.29Eb9010091000103.5Eb901007100001172Eb901010140002100.29Eb901010140002100.29Eb9010091000103.5Eb901007100001146Eb901010140002100.29Eb901010140002100.29Eb9010091000101.7Eb901007100001165Eb90"
def data_parse_basic(data):
	sensor_map = {"004": "ShiDu","005": "MenCi","007":"FengXiang","009":"FengLi","010":"DaQiYa","00D":"WenDu"} 

	try:
		value_dict = data.split("Eb90")
		#print value_dict
		#print len(value_dict[0])
		sensorList = []
		for value in value_dict:
			if len(value) > 10:
				pattern = re.compile(r"\d+\.*\d*")
				#print pattern
				match  = pattern.search(value)
				value = match.group()
				#print "value"
				#print value
				if len(value) > 10:
					sensor = dict()
					sensor["sensorType"] = sensor_map[value[1:4]]
					sensor["zigbeeId"] = value[6:10]
					sensor["sensorData"] = float(value[10:])
					sensorList.append(sensor)
				#print sensor
		
		#print sensorList
		tmpList = []
		tmpList.append(sensorList[0])
		tmpList[0]["count"] = 1

		for i in range(1,len(sensorList)):
			flag = False
			for j in range(0,len(tmpList)):
				if sensorList[i]["sensorType"] == tmpList[j]["sensorType"] and sensorList[i]["zigbeeId"] == tmpList[j]["zigbeeId"]:
					flag = True
					tmp = j
			if flag:
				tmpList[tmp]["sensorData"] = tmpList[tmp]["sensorData"] + sensorList[i]["sensorData"]
				tmpList[tmp]["count"] = tmpList[tmp]["count"] + 1
			else:
				sensorList[i]["count"] = 1
				tmpList.append(sensorList[i])

		#print tmpList
		for i in range(0,len(tmpList)):
			tmpList[i]["sensorData"] = round(tmpList[i]["sensorData"] / float(tmpList[i]["count"]),3) 
			tmpList[i]["sensorData"] = str(tmpList[i]["sensorData"])
			del tmpList[i]["count"]

		#print "tmpList: "
		#print tmpList
	except:
		tmpList = "None"

	#print "ok"
	#print "tmpList: "
	#print tmpList
	return tmpList
#data_parse_basic(data)

def data_parse(data):
	sensor_name = ["WenDu","MenCi","FengXiang","FengLi","DaQiYa","ShiDu","LiuSu"]
	tmpList = data_parse_basic(data);

	#if tmpList != "None":
	try:
		#print "OK"
		#print tmpList
		#print tmpList != "None"
		for i in range(0,len(tmpList)):
			del tmpList[i]["zigbeeId"]
	
		for key in sensor_name:
			flag = False
			default = {"sensorData":"none"}
			for i in range(0,len(tmpList)):
				if tmpList[i]["sensorType"] == key:
					flag = True
			if not flag:
				default["sensorType"] = key
				tmpList.append(default)
	
		sensorList = {}
		for i in range(0,len(tmpList)):
			sensorList[tmpList[i]["sensorType"]] = tmpList[i]["sensorData"]

	#else:
	except:
		sensorList = {"WenDu":"none","MenCi":"none","FengXiang":"none","FengLi":"none","DaQiYa":"none","ShiDu":"none","LiuSu":"none",}

	return sensorList
#print parseData_new(data)

def location_parse(data):
	try:
		lat_pattern = re.compile(r"LAT:\s*\+\d+\s*\d+\s*\d+")
		lng_pattern = re.compile(r"LNG:\s*\+\d+\s*\d+\s*\d+")
		
		lat = location_parse_gps_get(data,lat_pattern)
		lng = location_parse_gps_get(data,lng_pattern)

		#use gps api to covert the gps to coordinates of  baidu map 
		request = urllib2.Request("http://api.gpsspg.com/convert/latlng/?oid=326&key=76E87F2FE51418423FA87258742C5959&from=0&to=2&latlng=" + lat + "," + lng)
		response = urllib2.urlopen(request)
		response = response.read()
		response = json.loads(response)
		lat = response["result"][0]["lat"]
		lng = response["result"][0]["lng"]

		location = {}
		location["x"] = str(lat)
		location["y"] = str(lng)
		

	except ValueError as err:
		print str(err)
		location = {}
		location["x"] = "None"
		location["y"] = "None"


	return location

def location_parse_gps_get(data,pattern):
	match = pattern.search(data)
	gps= match.group()

	gps = gps.split(':')
	gps = gps[1].strip()

	gps = gps.split('+')
	(gps_degree, gps_minute, gps_second) = gps[1].split(' ')
	gps = str(int(gps_degree) + int(gps_minute) / 60 + int(gps_second) / 3600)

	return gps

#data = '2014-10-17:18-16-04'
def time_parse(data):
	dt = datetime.datetime.strptime(data,'%Y-%m-%d:%H-%M-%S')
	#date = data.split(':')

	#(year, month, day) = date[0].split('-')
	#(hour,minute,second) = date[1].split('-')

	#dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
	dt = dt.strftime("%Y-%m-%dT%H:%M:%SZ") 
	dt = str(dt)

	return dt
#print time_parse(data)



