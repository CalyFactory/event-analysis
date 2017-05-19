# -*- coding: utf-8 -*-
import konlpy
import nltk
import sys

from konlpy.tag import Mecab

from manager import db_manager

if len(sys.argv) < 2 :
	print("arguments length is 0. input string wanted analyzed.")
	sys.exit()

if len(sys.argv) > 2 :
	print("arguments length is over 2. input one string wanted analyzed.")
	sys.exit()

mecab = Mecab()

def analysis(sentence):
	# POS tag a sentence
	# sentence = u'만 6세 이하의 초등학교 취학 전 자녀를 양육하기 위해서는'
	result=[]
	words = konlpy.tag.Twitter().pos(sentence)

	# Define a chunk grammar, or chunking rules, then chunk
	grammar = """
	NP: {<N.*>*<Suffix>?}   # Noun phrase
	VP: {<V.*>*}            # Verb phrase
	AP: {<A.*>*}            # Adjective phrase
	"""
	parser = nltk.RegexpParser(grammar)
	chunks = parser.parse(words)
	"""
	print("# Print whole tree")
	print(chunks.pprint())
	print('')
	print("# pure print")
	print(chunks)
	print('')
	print("\n# Print noun phrases only")
	"""
	for subtree in chunks.subtrees():
		if subtree.label()=='NP':
			result.append(', '.join((e[0] for e in list(subtree))))
			#print(subtree.pprint())
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
#def listOfAnalysis()
# db_manager.query("select * from EVENT where calendar_hashkey ='caa746b0643e719a0a60080365520f4c946c49b0efbdb6ecd49ec99a'")

#analysis("헬로우 안녕 여러분들")
def PrinftKindsOfInput(inputMessage):
	print("----------------------")
	print("input : "+inputMessage)
	print()
	print()
	print("===== 형태소 ==========")
	print(mecab.morphs(inputMessage))
	print()

	print("===== 명사 ==========")
	print(mecab.nouns(inputMessage))
	print()

	print("===== 품사별 ==========")
	print("")
	print(mecab.pos(inputMessage))
	print()

PrinftKindsOfInput(str(sys.argv[1]))