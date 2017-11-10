from Porter import PorterStemmer
import itertools

from common import getDictFromFile
from common import dumpJsonToFile
from common import genericErrorInfo
from common import getTokenizer
from common import readTextFromFile

import networkx as nx

#CAUTION: duplicate with A3.P1.py
def searchKwordWindowsOpt(text, k, left, right, skipBothFlag=False):

	tokens = []
	try:
		tokens = getTokenizer(text)
	except:
		genericErrorInfo()

	counts = {'left': 0, 'both': 0}

	kWordWindows = []
	for i in range(len(tokens)):
		
		if( i % k == 0 ):
			kWordWindows.append([])

		kWordWindows[-1].append( tokens[i] )
	
	counts['left'] = len(kWordWindows)

	if( skipBothFlag == False ):
		for win in kWordWindows:
			if( left in win and right in win ):
				counts['both'] += 1

	return counts

def getPairs(l):
	return list(itertools.combinations(l, 2))

def getAssociationForPair(vocabDict, pair, windowSize):

	a, b = pair
	
	Na = 0
	Nb = 0
	Nab = 0
	
	if( vocabDict[a] and vocabDict[b] ):
		
		for f in vocabDict[a]['f']:
			f = f + '.txt'
			f = readTextFromFile(f)
			
			counts = searchKwordWindowsOpt(f, windowSize, a, b)
			
			Na += counts['left']
			Nab += counts['both']

		for f in vocabDict[b]['f']:
			counts = searchKwordWindowsOpt(f, windowSize, b, a, True)
			Nb += counts['left']

	
	if( Nab != 0 ):
		return Nab / (Na + Nb)
	else:
		return -1

	

def optimizeStemClass(oldStemClass, windowSize, threshold):
	
	'''
		Algorithm from: Search Engines Information Retrieval in Practice (page 191-192)
	'''
	vocabDict = getDictFromFile('wiki-small-vocab.json')
	counter = 0
	total = len(oldStemClass)
	for stem, classList in oldStemClass.items():
		
		pairs = getPairs(classList)
		
		'''
			Construct a graph where the vertices represent words and the edges are between
			words whose co-occurrence metric is above a threshold T.
		'''
		G = nx.Graph()
		G.add_nodes_from(classList)

		for i in range(len(pairs)):
			
			'''
				Compute a co-occurrence or association metric for each pair. This measures
				how strong the association is between the words.
			'''
			dice = getAssociationForPair(vocabDict, pairs[i], windowSize)
			
			if( dice >= threshold ):
				G.add_edge( pairs[i][0], pairs[i][1] )

		if( counter % 10 == 0 ):
			print(counter, 'of', total, 'dice:', dice, '\n')
		
		if( len(G.edges()) != 0 ):
			
			print('Graph:')
			print('nodes:', G.nodes())
			print('edges:', G.edges())

			conComp = list(nx.connected_component_subgraphs(G))
			
			print()
			print('New stem class for stem:', stem, ':')
			for subgraph in conComp:
				
				subgraph = subgraph.nodes()
				if( len(subgraph) > 1 ):
					print('\t', subgraph)

		counter += 1
		

def getStemsClassesSizeKPlus(k=2):

	stemClasses = getDictFromFile('wiki-small-vocab-stem-classes.json')
	chosenStemClasses = {}

	for stem, classList in stemClasses.items():
		if( len(classList) >= k ):
			chosenStemClasses[stem] = classList

	diff = len(stemClasses) - len(chosenStemClasses)

	print('old:', len(stemClasses))
	print('new:', len(chosenStemClasses))
	print('getStemsClassesSizeKPlus() - diff:', diff, '\n')
	return chosenStemClasses

def getStemclasses():
	
	stemClasses = {}
	vocabDict = getDictFromFile('wiki-small-vocab.json')
	counter = 0
	
	for voc, vocDict in vocabDict.items():
			
		stem = PorterStemmer.useStemer(voc)
		stemClasses.setdefault(stem, [])
		stemClasses[stem].append(voc)

		if( counter % 10000 == 0 ):
			print('\t', counter, voc)

		counter += 1

	dumpJsonToFile('wiki-small-vocab-stem-classes.json', stemClasses, False)


#generates a dictionary with stem as key, and value as list of terms that map to the stem (stem classes)
#getStemclasses()

#create new stem classed
#sizeOfStemClass = 2
#chosenStemClasses = getStemsClassesSizeKPlus(sizeOfStemClass)

#windowSize = 80
#threshold = 0.003
#optimizeStemClass(chosenStemClasses, windowSize, threshold)

