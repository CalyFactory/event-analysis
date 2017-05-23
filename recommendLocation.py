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

		m = t.parseToNode(sentence)
		while m:
			if (m.feature.find("지하철") > 0) or (m.feature.find("동이름") > 0) or (m.feature.find("대학교") > 0):
				#print(m.surface, "\t", m.feature)
				if result is not '':
					result = result + ', '
				result=result+m.surface
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


