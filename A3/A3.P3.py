from common import getDictFromFile
from Porter import PorterStemmer
import itertools

def getPairs(l):
	return list(itertools.combinations(l, 2))

def isWord(term):

	term = term.strip()
	for t in term:
		if( t.isalpha() == False ):
			return False

	return True

def getKAlphabeticalWords(k = 1000):

	index = getDictFromFile('wiki-small-vocab.json')
	sortedKeys = list(index.keys())
	sortedKeys.sort()

	counter = 0	
	for i in range(len(sortedKeys)):
		
		if( isWord(sortedKeys[i]) == True ):
			counter += 1

			print(sortedKeys[i])


		if( counter == 1000 ):
			break

def getStemclasses():

	stemClasses = {}
	infile = open('good-1000-words.txt', 'r')
	terms = infile.readlines()
	infile.close()

	for voc in terms:
		voc = voc.strip()
			
		stem = PorterStemmer.useStemer(voc)
		stemClasses.setdefault(stem, [])
		stemClasses[stem].append(voc)

	return stemClasses

def getAssociationForPair(vocabDict, pair):

	a, b = pair
	
	Na = 0
	Nb = 0
	Nab = 0
	
	if( vocabDict[a] and vocabDict[b] ):
		
		aFileSet = set(vocabDict[a]['f'])
		bFileSet = set(vocabDict[b]['f'])

		Na = len(aFileSet)
		Nb = len(bFileSet)
		Nab = len(aFileSet & bFileSet)
	
	if( Nab != 0 ):
		return Nab / (Na + Nb)
	else:
		return 0

def compAssocForPairsInStemClass(stemClasses):
	
	vocabDict = getDictFromFile('wiki-small-vocab.json')
	counter = 0
	total = len(stemClasses)

	for stem, classList in stemClasses.items():
		
		#only consider stem classes with multiple members
		if( len(classList) < 2 ):
			continue

		pairs = getPairs(classList)
		print('stem:', stem)
		print('\tstem class:', classList, '\n')
		for i in range(len(pairs)):
			
			'''
				Compute a co-occurrence or association metric for each pair. This measures
				how strong the association is between the words.
			'''
			dice = getAssociationForPair(vocabDict, pairs[i])

			print('\tpair:', pairs[i])
			print('\tdice:', dice)
			print('\t', counter, 'of', total, '\n')

		print()
		counter += 1


k = 1000
getKAlphabeticalWords(k)


stemClasses = getStemclasses()


compAssocForPairsInStemClass(stemClasses)


threshold = 0.002
compAssocForPairsInStemClassThreshold(stemClasses, threshold)