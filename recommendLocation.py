# -*- coding: utf-8 -*-
#import konlpy
#import nltk
import sys

import MeCab
import string

from manager import db_manager
"""
if len(sys.argv) < 2 :
	print("arguments length is 0. input string wanted analyzed.")
	sys.exit()

if len(sys.argv) > 2 :
	print("arguments length is over 2. input one string wanted analyzed.")
	sys.exit()
"""
def analysis(sentence,startDt, endDt):
	result=''
	purposeResult=''
	locationCount=0
	locationsJson={}
	splitedStartDt=str(startDt).split(' ')
	splitedEndDt=str(endDt).split(' ')
	timeZoneJson={
		'event_start':'',
		'event_end':'',
		'event_start':splitedStartDt[1][:5],
		'event_end':splitedEndDt[1][:5]
	}
	eventTypesJson={}
	timeZone={
		'아침':'7시',
		'브런치':'11시',
		'점심':'13시',
		'저녁':'19시',
		'밤':'22시'
	}
	purposeIndex = {
		'CPI01':0,
		'CPI02':0,
		'CPI03':0,
		'CPI04':0,
		'CPI05':0,
		'CPI06':0
	}
	printPurpose = {
		'CPI01':'지인과의 약속',
		'CPI02':'데이트 일정',
		'CPI03':'각종 기념일',
		'CPI04':'모임 뒷풀이',
		'CPI05':'회의 및 스터디',
		'CPI06':'문화생활'	
	}
	try:
	    #print(MeCab.VERSION)

		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
		#print(t.parse(sentence))
		t.parse(sentence)
		time = -1
		CPICount=0
		m = t.parseToNode(sentence)
		while m:
			if result is not '':
				result = result + ', '

			### Grep time-zone : ical / line_plus@naver.com
			if m.feature.find('SN') > -1 and m.surface.isdigit():
				time=m.surface
			elif m.feature.find('NNBC') > -1 and m.feature.find('시') > -1 and time is not -1:
				endTime = int(time)+1
				if int(time) < 10:
					time = '0'+str(time)
				if int(endTime) < 10:
					endTime = '0'+str(endTime)
				timeZoneJson['extract_start']=str(time)+':00'
				timeZoneJson['extract_end']=str(endTime)+':00'
			elif (m.surface.find('아침') > -1) or (m.surface.find('브런치') > -1) or (m.surface.find('점심') > -1) or (m.surface.find('저녁') > -1) or (m.surface.find('밤') > -1):
				time=timeZone[m.surface]

			### Grep purpose
			elif m.feature.find('CPI') > -1:
				if CPICount > 1:
					continue

				partsOfFeature = m.feature.split(',')
				for part in partsOfFeature:
					if part.find('CPI') > -1:
						if purposeIndex[part] > 0:
							continue
						purposeIndex[part]=purposeIndex[part]+1
						eventTypesJson[CPICount]={"id":part}
						CPICount=CPICount+1
						purposeResult=purposeResult+' '+printPurpose[part]

			### Grep location : google / calyfactorytester3@gmail.com
			elif (m.feature.find("대학교") > -1):
				if m.surface.find("대학교") > -1:
					result=result+m.surface
					print("Catch : "+m.surface)
				else:
					partsOfFeature = m.feature.split(',')
					#print(partsOfFeature)
					for part in partsOfFeature:
						if part.find('대학교') > 0:
							result=result+part
							print("Catch : "+part)
							break	
			elif (m.feature.find("지하철") > -1) and (m.surface.find("역") < 0 or m.surface == '동역사'):
				partsOfFeature = m.feature.split(',')
				#print(partsOfFeature)
				for part in partsOfFeature:
					if part.find('역') > -1:
						locationsJson[locationCount]={'no':locationCount,'region':part}
						locationCount = locationCount + 1
						result=result+part
						break
			elif m.feature.find("지하철") > -1:
				locationsJson[locationCount]={'no':locationCount,'region':m.surface}
				locationCount = locationCount + 1
				#print(m.surface, "\t", m.feature)

			elif m.feature.find("동이름") > 0:
				result=result+m.surface
			else:
				#print('else : '+m.surface+'/ '+m.feature)
				pass

			m = m.next

	except RuntimeError as e:
		print("RuntimeError:", e)


	if time is -1:
		timeZoneJson['extract_start']='None'
		timeZoneJson['extract_end']='None'
	if CPICount is 0:
		eventTypesJson="None"
	if locationCount is 0:
		locationsJson="None"
	jsonTest = {
		'locations': locationsJson,
		'time_set': timeZoneJson, 
		'event_types':eventTypesJson
	}
	return jsonTest
	#return [result,time,purposeResult]

def testAnalysis(eventHashKey):
	rows = db_manager.query("select "
		"E.summary,E.start_dt,E.end_dt,E.location "
	"from EVENT as E "
	"where"
		" E.event_hashkey = '"+eventHashKey+"'"
	)

	for row in rows:
		argSummary = row.summary
		if row.location is not None:
			argSummary = argSummary+' '+row.location

		return analysis(argSummary, row.start_dt, row.end_dt)
