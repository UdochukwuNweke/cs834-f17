import math
from P2 import getHTMLPaths
from datetime import datetime

from common import getTextFromHTML
from common import readTextFromFile
from common import dumpJsonToFile
from common import getDictFromFile
from common import writeTextToFile
from common import genericErrorInfo
from common import getTokenizer

from sklearn.feature_extraction.text import CountVectorizer
import re
import sys

def getKwordWindows(text, k):

	tokens = []
	try:
		tokens = getTokenizer(text)
	except:
		genericErrorInfo()

	kWordWindows = []
	for i in range(len(tokens)):
		
		if( i % k == 0 ):
			kWordWindows.append([])

		kWordWindows[-1].append( tokens[i] )

	
	return kWordWindows

def getKwordWindowsOpt(text, k):

	tokens = []
	try:
		tokens = getTokenizer(text)
	except:
		genericErrorInfo()

	kWordWindows = []
	for i in range(len(tokens)):
		
		if( i % k == 0 ):
			kWordWindows.append([])

		kWordWindows[-1].append( tokens[i] )

	
	return kWordWindows






def transformDocToWindow(vocabDict, vocab):

	if( vocab not in vocabDict ):
		print('term:', vocab, 'not in vocab')
		return

	allWindows = []
	for i in range(len(vocabDict[vocab]['f'])):
		f = vocabDict[vocab]['f'][i] + '.txt'
		f = readTextFromFile(f)
		
		allWindows += getKwordWindows(f, 5)

	vocabDict[vocab]['f'] = allWindows

def transformDocToWindowOpt(vocabDict, vocab):

	if( vocab not in vocabDict ):
		print('term:', vocab, 'not in vocab')
		return

	allWindows = {'tot': 0, 'windows': []}
	for i in range(len(vocabDict[vocab]['f'])):
		f = vocabDict[vocab]['f'][i] + '.txt'
		f = readTextFromFile(f)
		
		allWindows['windows'] += getKwordWindowsOpt(f, 5)

	
	allWindows['tot'] = len(allWindows['windows'])
	windowsWithVocab = []

	for win in allWindows['windows']:
		if(vocab in win):
			windowsWithVocab.append(win)

	allWindows['windows'] = windowsWithVocab
	vocabDict[vocab]['f'] = allWindows



def countTerms(windows, left, right):
		
	count = {'left': 0, 'both': 0}
	
	for window in windows:		
		
		if(left in window):
			count['left'] += 1
			
			if(right in window):
				count['both'] += 1

	return count 

	

def getAssocMeasuresWindow(a, N, filename, k=10):

	prev = datetime.now()

	vocabDict = getDictFromFile(filename)	
	a = a.lower()
	
	if( a not in vocabDict ):
		print('term:', a, 'not in vocab')
		return
	
	transformDocToWindowOpt(vocabDict, a)
	totalVocab = len(vocabDict)
	pos = 0
	
	vocabDict[a]['MIM'] = -1
	vocabDict[a]['EMIM'] = -1
	vocabDict[a]['CHI-SQUARE'] = -1
	vocabDict[a]['DICE'] = -1

	for b, bDict in vocabDict.items():
		
		pos += 1
		
		if( b == a ):
			continue


		count = countTerms( vocabDict[a]['f']['windows'], a, b )
		Na = count['left']
		Nab = count['both']

		transformDocToWindowOpt(vocabDict, b)
		count = countTerms( vocabDict[b]['f']['windows'], b, a )
		Nb = count['left']

		MIM = -1
		EMIM = -1
		dice = -1
		chiSquare = -1

		if( pos % 100 == 0 ):
			print(pos, 'of', totalVocab)
			print('\tNa:', Na, a)
			print('\tNb:', Nb, b)
			print('\tNab:', Nab)
			delta = datetime.now() - prev
			print('\ttotal seconds:', delta.seconds)

		NaTimesNb = Na * Nb

		if( Nab != 0 ):
			MIM = Nab / (Na * Nb)
			dice = Nab / (Na + Nb)
			EMIM = Nab * math.log(N * MIM, 10)

		if( NaTimesNb != 0 ):
			numer = Nab - (NaTimesNb/N)
			chiSquare = (numer * numer) / NaTimesNb


		bDict['MIM'] = MIM
		bDict['EMIM'] = EMIM
		bDict['CHI-SQUARE'] = chiSquare
		bDict['DICE'] = dice

	for sortCriteria in ['MIM', 'EMIM', 'CHI-SQUARE', 'DICE']:

		print()

		sort = sorted( vocabDict.items(), key=lambda x: x[1][sortCriteria], reverse=True)
		sort = sort[:k]
		
		print(a, 'vs')
		for termDict in sort:
			term, termDict = termDict
			print('\tterm:', term, sortCriteria + ':', termDict[sortCriteria])
		

		
		
	



def getAssocMeasuresDocs(a, N, k = 10):

	
	vocabDict = getDictFromFile('wiki-small-vocab.json')
	a = a.lower()
	
	if( a not in vocabDict ):
		print('term:', a, 'not in vocab')
		return

	aFileSet = set(vocabDict[a]['f'])
	vocabDict[a]['MIM'] = -1
	vocabDict[a]['EMIM'] = -1
	vocabDict[a]['CHI-SQUARE'] = -1
	vocabDict[a]['DICE'] = -1

	Na = len(aFileSet)

	for b, bDict in vocabDict.items():
		
		if( b == a ):
			continue

		bFileSet = set(bDict['f'])
		Nb = len(bFileSet)
		intersect = aFileSet & bFileSet

		MIM = -1
		EMIM = -1
		dice = -1
		chiSquare = -1

		Nab = len(intersect)
		NaTimesNb = Na * Nb

		if( Nab != 0 ):
			
			MIM = Nab / (Na * Nb)
			dice = Nab / (Na + Nb)
			EMIM = Nab * math.log(N * MIM, 10)
		
		if( NaTimesNb != 0 ):
			numer = Nab - (NaTimesNb/N)
			chiSquare = (numer * numer) / NaTimesNb

		bDict['MIM'] = MIM
		bDict['EMIM'] = EMIM
		bDict['CHI-SQUARE'] = chiSquare
		bDict['DICE'] = dice

	
	for sortCriteria in ['MIM', 'EMIM', 'CHI-SQUARE', 'DICE']:

		print()

		sort = sorted( vocabDict.items(), key=lambda x: x[1][sortCriteria], reverse=True)
		sort = sort[:k]
		
		print(a, 'vs')
		counter = 1
		for termDict in sort:
			term, termDict = termDict
			print('\t', counter, 'term:', term, sortCriteria + ':', termDict[sortCriteria])
			counter += 1
	
	

def getVocabFreqDict(filenames, stop, ngramTup=(1, 1)):

	vocabDict = {}

	for i in range( len(filenames) ):
		f = filenames[i].strip()

		html = readTextFromFile(f)
		text = getTextFromHTML(html)
		#writeTextToFile(f + '.txt', text)

		if( len(text) == 0 ):
			continue
		
		countVectorizer = CountVectorizer( min_df=1, stop_words='english', ngram_range=ngramTup )
		termFreqMat = countVectorizer.fit_transform([text])

		for term in list(countVectorizer.vocabulary_.keys()):
			vocabDict.setdefault(term, {'f': []})
			vocabDict[term]['f'].append(f)
		
		if( i % 100 == 0 ):
			print( i, 'of', len(filenames) )

		if( i > stop ):
			break

	return vocabDict



stop = 500
filenames = getHTMLPaths()
vocabDict = getVocabFreqDict(filenames, stop)
dumpJsonToFile('wiki-small-vocab-' + str(stop)  +'.json', vocabDict, False)





word = 'hospital'
N = 6042
k = 20
getAssocMeasuresDocs(word, N, k)


'''
#command line: python A3.P1.py
if( len(sys.argv) > 1 ):
	filename = 'wiki-small-vocab.json'
	word = sys.argv[1]
	N = 15103
	k = 20
	getAssocMeasuresWindow(word, N, filename, k)
'''




