# -*- coding: utf-8 -*-
#import konlpy
#import nltk
import sys

#from konlpy.tag import Mecab
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
def analysis(sentence):
	result='';
	try:
	    #print(MeCab.VERSION)

		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
		#print(t.parse(sentence))
		t.parse(sentence)
		time = -1;
		m = t.parseToNode(sentence)
		while m:
			if result is not '':
				result = result + ', '

			### Grep time-zone
			"""
			if m.surface.isdigit():
				tmpList = m.feature.split(',')
				isSN=False
				for item in tmpList:
					if item.find('SN') is not -1:
						isSN=True
				if isSN is True:
					time=m.surface
			if m.feature.find("시") 
			"""
			if m.feature.find('SN') > -1 and m.surface.isdigit():
				time=m.surface
			elif m.feature.find('NNBC') > -1 and m.feature.find('시') > -1 and time is not -1:
				# assign time data
				pass
			##
			# Grep location
			elif (m.feature.find("대학교") > -1):
				if m.surface.find("대학교") > -1:
					result=result+m.surface
				else:
					partsOfFeature = m.feature.split(',')
					print(partsOfFeature)
					for part in partsOfFeature:
						if part.find('대학교') > -1:
							result=result+part
							break	
			elif (m.feature.find("지하철") > -1) and (m.surface.find("역") < 0 or m.surface == '동역사'):
				partsOfFeature = m.feature.split(',')
				print(partsOfFeature)
				for part in partsOfFeature:
					if part.find('역') > -1:
						result=result+part
						break
			elif (m.feature.find("지하철") > -1) or (m.feature.find("동이름") > 0):
				#print(m.surface, "\t", m.feature)
				result=result+m.surface
			else:
				print('else : '+m.surface+'/ '+m.feature)

			m = m.next

	except RuntimeError as e:
	    print("RuntimeError:", e)

	return result


def listFromAccount(account):
	loginPlatform, userId = account.split('/')
	result=[]
	rows = db_manager.query("select "
		"E.summary,E.start_dt,E.end_dt,E.location "
	"from EVENT as E "
	"inner join CALENDAR as C on E.calendar_hashkey = C.calendar_hashkey "
	"inner join USERACCOUNT as UA on C.account_hashkey = UA.account_hashkey "
	"where "
		"UA.login_platform = '"+loginPlatform+"' "
		"and UA.user_id = '"+userId+"'"
	"order by E.start_dt ASC")

	for row in rows:
		result.append({
			'summary':row.summary,
			'start_dt':row.start_dt,
			'end_dt':row.end_dt,
			'location':row.location,
			'analysis':analysis(row.summary)
		})
	return result

def listFromAccountByCalendarHashkey(account):
	result=[]
	rows = db_manager.query("select "
		"E.summary,E.start_dt,E.end_dt,E.location "
	"from EVENT as E "
	"inner join CALENDAR as C on E.calendar_hashkey = C.calendar_hashkey "
	"inner join USERACCOUNT as UA on C.account_hashkey = UA.account_hashkey "
	"where "
		"C.calendar_hashkey = '"+account+"'"
	"order by E.start_dt ASC")
	for row in rows:
		result.append({
			'summary':row.summary,
			'start_dt':row.start_dt,
			'end_dt':row.end_dt,
			'location':row.location,
			'analysis':analysis(row.summary)
		})
	return result


