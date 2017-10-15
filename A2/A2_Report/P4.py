from P2 import getHTMLPaths

from common import readTextFromFile
from common import getTextFromHTML

from sklearn.feature_extraction.text import CountVectorizer

def getHeapsData(filenames):
	

	outfile = open('vocabWordCount.csv', 'w')
	outfile.write('Vocab,WordCount\n')

	totalVocab = set()
	wordCount = 0
	for i in range( len(filenames) ):
		f = filenames[i].strip()
		html = readTextFromFile(f)
		text = getTextFromHTML(html)

		if( len(text) == 0 ):
			continue
		
		countVectorizer = CountVectorizer( min_df=1, stop_words='english', 
		ngram_range=(1,2) )
		termFreqMat = countVectorizer.fit_transform([text])

		totalVocab = totalVocab.union( set(countVectorizer.vocabulary_.keys()) )
		wordCount += termFreqMat.todense().sum()
		
		outfile.write( str(len(totalVocab)) + ', ' + str(wordCount) + '\n' )

		if( i % 100 == 0 ):
			print( i, 'of', len(filenames) )

	outfile.close()

filenames = getHTMLPaths()
getHeapsData( filenames )