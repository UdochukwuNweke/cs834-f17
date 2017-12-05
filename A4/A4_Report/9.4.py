import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#spam dataset: https://archive.ics.uci.edu/ml/datasets/YouTube+Spam+Collection

def getInput(filename):

	infile = open(filename, 'r')
	lines = infile.readlines()
	infile.close()

	del lines[0]

	spamClassDict = {}
	spamClassDict['NOT'] = []
	spamClassDict['SPAM'] = []
	for line in lines:
		line = line.strip().split(' <> ')
		
		doc = line[0].strip()
		spamClass = line[1].strip()

		if( spamClass == '0' ):
			spamClassDict['NOT'].append(doc)
		else:
			spamClassDict['SPAM'].append(doc)

	return spamClassDict

def getTFMatrix(docList):
	np.set_printoptions(threshold=np.nan, linewidth=110)

	count_vectorizer = CountVectorizer(ngram_range=(1,1))
	term_freq_matrix = count_vectorizer.fit_transform(docList)
	
	sortedVocab = sorted(count_vectorizer.vocabulary_.items(), key=lambda x: x[1])
	
	#print( sortedVocab )
	#print( term_freq_matrix.todense() )

	return {'docMat': term_freq_matrix.todense().tolist(), 'vocab': sortedVocab}

def getTermIndexFromVocab(word, vocab):

	for term in vocab:
		term, index = term
		
		if( word == term ):
			return index
	
	return -1

def calcMultinomial(w, c, trainingSet):

	C = 0
	df_wc = 0	
	
	wi = getTermIndexFromVocab(w, trainingSet['vocab'])

	if( wi != -1 ):
		start = 0
		end = 0
		
		if( c == 'NOT' ):
			#search non spam class
			start = 0
			end = 175
		else:
			#search spam class
			start = 175
			end = len(trainingSet['docMat'])

		for i in range(start, end):
			vec = trainingSet['docMat'][i]
			df_wc += vec[wi]
			C += sum(vec)
	else:
		#print('Not found in vocab')
		pass

	if( C != 0 ):
		return df_wc/C
	else:
		return 0

def calcMultBernoulli(w, c, trainingSet):

	N_c = 0
	df_wc = 0	
	
	wi = getTermIndexFromVocab(w, trainingSet['vocab'])

	if( wi != -1 ):
		start = 0
		end = 0
		
		if( c == 'NOT' ):
			#search non spam class
			start = 0
			end = 175
		else:
			#search spam class
			start = 175
			end = len(trainingSet['docMat'])

		for i in range(start, end):
			N_c += 1
			vec = trainingSet['docMat'][i]
			if( vec[wi] != 0 ):
				df_wc += 1
			
	else:
		#print('Not found in vocab')
		pass

	p = df_wc/N_c
	#print('df_wc:', df_wc)
	#print( 'P(w|c) = P(' + w + '|' + c + ') = ' + str(p) )
	return p

def testProbModels(trainingSet):

	for term in trainingSet['vocab']:
		term = term[0]
		print('\n')
		print('*' * 50)
		print('Multiple-Bernoulli')
		print('\t' + term)
		print('\t\tP(SPAM) = ', calcMultBernoulli(term, 'SPAM', trainingSet))
		print('\t\tP(NOT) = ', calcMultBernoulli(term, 'NOT', trainingSet))

		print('\nMultinomial')
		print('\t\tP(SPAM) = ', calcMultinomial(term, 'SPAM', trainingSet))
		print('\t\tP(NOT) = ', calcMultinomial(term, 'NOT', trainingSet))

filename = 'Youtube02-KatyPerry.csv'
spamClassDict = getInput(filename)

dataset = spamClassDict['NOT'] + spamClassDict['SPAM']
trainingSet = getTFMatrix(dataset)

testProbModels(trainingSet)

#print( spamClassDict['0'] )
#print(spamClassDict)