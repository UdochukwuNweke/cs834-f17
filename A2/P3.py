from P2 import getHTMLPaths
from common import readTextFromFile
from common import getTextFromHTML
from common import dumpJsonToFile
from common import getDictFromFile

from sklearn.feature_extraction.text import CountVectorizer

def genCSVFile():

	outfile = open('sorted-1-2-gram.org.csv', 'w')
	outfile.write('Rank,Term,Freq,C\n')

	gramsDict = getDictFromFile('1-2-gram.json')
	sortedDict = sorted(gramsDict.items(), key=lambda x: x[1], reverse=True)
	
	total = 770552
	rank = 1
	for tup in sortedDict:
		term, freq = tup
		c = (freq/total) * rank
		outfile.write( str(rank) + ', ' + term + ', ' + str(freq) + ', ' + str(round(c, 5)) + '\n' )
		rank += 1

	outfile.close()


def getVocabFreqDict(filenames):

	vocabDict = {}

	for i in range( len(filenames) ):
		f = filenames[i].strip()
		html = readTextFromFile(f)
		text = getTextFromHTML(html)

		if( len(text) == 0 ):
			continue
		
		countVectorizer = CountVectorizer( min_df=1, stop_words='english', ngram_range=(1,2) )
		termFreqMat = countVectorizer.fit_transform([text])

		for term in list(countVectorizer.vocabulary_.keys()):
			vocabDict.setdefault(term, 0)
			vocabDict[term] += 1
		
		if( i % 100 == 0 ):
			print( i, 'of', len(filenames) )

	dumpJsonToFile( '1-2-gram.json', vocabDict )
	

#get ngram (1, 2) dictionary
#filenames = getHTMLPaths()
#getVocabFreqDict(filenames)

genCSVFile()