import sys
import json 
from pathlib import Path
from manager import db_manager

def loadSubwayDict():
	regionDict={}
	regionRows = db_manager.query('select station_name, old_address from SUBWAY_INFO')

	for row in regionRows:
		if type(row.old_address) is str:
			splitedAddress = row.old_address.split(' ')
			
			# 해당 키의 항목이 있으면, 해당 값에 append
			if splitedAddress[2] in regionDict:
				isExist=False
				for item in regionDict[splitedAddress[2]]:
					if item == row.station_name+'역':
						isExist=True
						break

				if isExist is False:
					regionDict[splitedAddress[2]].append(row.station_name+'역')
			# 해당 키의 항목이 없으면, 새로운 리스트 형태로 추가
			else:
				regionDict[splitedAddress[2]]=[row.station_name+'역']

	with open('./key/region.json') as extraRegionJson:
	    extraRegionDict = json.load(extraRegionJson)

	for extraRegion in extraRegionDict.keys():
		regionDict[extraRegion]=extraRegionDict[extraRegion]

	univDict={}
	univRows = db_manager.query('select univ_name, old_address from UNIV_INFO')

	for row in univRows:
		if type(row.old_address) is str:
			splitedAddress = row.old_address.split(' ')
		
			univDict[row.univ_name]=splitedAddress[2]

	return [regionDict, univDict]