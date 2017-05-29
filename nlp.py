# -*- coding: utf-8 -*-
#import konlpy
#import nltk
import sys

#from konlpy.tag import Mecab
import MeCab
import string

from manager import db_manager

if len(sys.argv) < 2 :
	print("arguments length is 0. input string wanted analyzed.")
	sys.exit()

if len(sys.argv) > 2 :
	print("arguments length is over 2. input one string wanted analyzed.")
	sys.exit()

def extractTime(sentence):
	try:

		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
		m = t.parseToNode(sentence)
		while m:
			print(m.surface, "\t", m.feature)
			m = m.next

		print("EOS")
		print()
		lattice = MeCab.Lattice()
		t.parse(lattice)
		lattice.set_sentence(sentence)
		len = lattice.size()
		for i in range(len + 1):
			b = lattice.begin_nodes(i)
			e = lattice.end_nodes(i)
			while b:
				print("B[%d] %s\t%s" % (i, b.surface, b.feature))
				b = b.bnext 
			while e:
				print("E[%d] %s\t%s" % (i, e.surface, e.feature))
				e = e.bnext 
		print("EOS")
		print()
		d = t.dictionary_info()
		while d:
			print("filename: %s" % d.filename)
			print("charset: %s" %  d.charset)
			print("size: %d" %  d.size)
			print("type: %d" %  d.type)
			print("lsize: %d" %  d.lsize)
			print("rsize: %d" %  d.rsize)
			print("version: %d" %  d.version)
			d = d.next
			
	except RuntimeError as e:
		print("RuntimeError:", e)	

def extractLocation(sentence):
	try:
		#print(MeCab.VERSION)

		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
		#print(t.parse(sentence))
		t.parse(sentence)

		m = t.parseToNode(sentence)
		while m:
			if (m.feature.find("동이름") > 0) or (m.feature.find("대학교") > 0):
				print(m.surface, "\t", m.feature)
			elif (m.feature.find("지하철") > 0):
				partsOfFeature = m.feature.split(',')
				
				for part in partsOfFeature:
					if part.find('역') > 0:
						print(part)
						break

			m = m.next


		"""
	    lattice = MeCab.Lattice()
	    t.parse(lattice)
	    lattice.set_sentence(sentence)
	    len = lattice.size()
	    for i in range(len + 1):
	        b = lattice.begin_nodes(i)
	        e = lattice.end_nodes(i)
	        while b:
	            #print("B[%d] %s\t%s" % (i, b.surface, b.feature))
	            b = b.bnext 
	        while e:
	            #print("E[%d] %s\t%s" % (i, e.surface, e.feature))
	            e = e.bnext 

	    d = t.dictionary_info()
	    while d:
	        print("filename: %s" % d.filename)
	        print("charset: %s" %  d.charset)
	        print("size: %d" %  d.size)
	        print("type: %d" %  d.type)
	        print("lsize: %d" %  d.lsize)
	        print("rsize: %d" %  d.rsize)
	        print("version: %d" %  d.version)
	        d = d.next
	    """
		
	except RuntimeError as e:
		print("RuntimeError:", e)

print("Import Mecab success with "+str(sys.argv[1]))


sentence = str(sys.argv[1])
extractTime(sentence)
