import matplotlib.pyplot as plt
import numpy as np

#https://gist.github.com/bwhite/3726239
def r_precision(r):
    """Score is precision after all relevant documents have been retrieved
    Relevance is binary (nonzero is relevant).
    >>> r = [0, 0, 1]
    >>> r_precision(r)
    0.33333333333333331
    >>> r = [0, 1, 0]
    >>> r_precision(r)
    0.5
    >>> r = [1, 0, 0]
    >>> r_precision(r)
    1.0
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        R Precision
    """
    r = np.asarray(r) != 0
    z = r.nonzero()[0]
    if not z.size:
        return 0.
    return np.mean(r[:z[-1] + 1])

#https://gist.github.com/bwhite/3726239


#https://gist.github.com/bwhite/3726239
def ndcg_at_k(r, k, method=0):
	"""Score is normalized discounted cumulative gain (ndcg)
	Relevance is positive real values.  Can use binary
	as the previous methods.
	Example from
	http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
	>>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
	>>> ndcg_at_k(r, 1)
	1.0
	>>> r = [2, 1, 2, 0]
	>>> ndcg_at_k(r, 4)
	0.9203032077642922
	>>> ndcg_at_k(r, 4, method=1)
	0.96519546960144276
	>>> ndcg_at_k([0], 1)
	0.0
	>>> ndcg_at_k([1], 2)
	1.0
	Args:
		r: Relevance scores (list or numpy) in rank order
			(first element is the first item)
		k: Number of results to consider
		method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
				If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
	Returns:
		Normalized discounted cumulative gain
	"""
	dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
	if not dcg_max:
		return 0.
	return dcg_at_k(r, k, method) / dcg_max

def plotOriginalPoints(masterPntCol):

	fig = plt.figure()
	fig.suptitle('Recall-Precision graph at 5. No. of relevant docs for recall is 16',
	 fontsize=14, fontweight='bold')

	ax = fig.add_subplot(111)
	fig.subplots_adjust(top=0.85)
	
	ax.set_xlabel('Recall')
	ax.set_ylabel('Precision')

	for lstOfPnts in masterPntCol:
		#Original points
		X = np.array(lstOfPnts)

		#plot points
		ax.plot(X[:,1], X[:,0])

	#set window size
	ax.axis([0, 1.02, 0, 1.02])

	#save plot
	plt.savefig('samplePlot.png')

def genPrecRecallGraph(query, K, data):

	twoDpnt = []
	
	allPr = calcPrecRecallAtK(query, K, data, 'list')
	for pr in allPr:
		twoDpnt.append([pr['precision'], pr['recall']])

	return twoDpnt

def calcPrecRecallAtK(query, K, data, returnType='single'):

	#16 relevant documents/query in CACM: 
	#http://www.cs.sfu.ca/CourseCentral/456/jpei/web%20slides/L19%20-%20Evaluation.pdf
	foundFlag = False

	relCount = 0
	count = 0
	precAtK = 0
	recallAtK = 0
	precisionRecallLst = []
	for q in data:
		
		if( q[0] == query ):
			foundFlag = True
			relCount += 1
			#print('g:', relCount, q)
		else:
			if( foundFlag ):
				#print('b')
				pass

		if( foundFlag ):
			count += 1
			
			precAtK = relCount/float(count)
			recallAtK = relCount/float(16)

			#print('precision@' + str(count) + ' =', precAtK)
			#print('recall@' + str(count) + ' =', recallAtK)
		
			precisionRecallLst.append({'precision': precAtK, 'recall': recallAtK})
		
		if( count == K ):
			break

	if( returnType == 'single' ):
		return {'precision': precAtK, 'recall': recallAtK}
	else:
		return precisionRecallLst

def calcAvgPrecForQuery(query, K, data):
	
	foundFlag = False

	relCount = 0
	count = 0
	avgPrecision = 0
	for q in data:
		
		if( q[0] == query ):
			foundFlag = True
			relCount += 1
			#print('g:', relCount, q)
		else:
			if( foundFlag ):
				#print('b')
				pass

		if( foundFlag ):
			count += 1
			#print('precision@' + str(count) + ' =', relCount/count)
			avgPrecision += relCount/float(count)

		if( count == K ):
			break

	return avgPrecision/float(K)



def getRankingForQuery(query, K, data):

	count = 0
	foundFlag = False
	ranking = []
	for q in data:

		if( q[0] == query ):
			foundFlag = True
			ranking.append(1)
		else:
			if( foundFlag ):
				#start populating from first find
				ranking.append(0)
		
		if( foundFlag ):
			count += 1

		if( count == K ):
			break

	return ranking


lines = getInput()
MAP = 0
rPrecision = 0
#for all gueries get MAP (5 and 10), average NDCG at 5 and 10, precision at 10
for query in range(1, 65):
	print 'query: ' + str(query)
	
	#mean average precision (MAP) 
	MAP += calcAvgPrecForQuery(query, 10, lines)
	
	#precision at 10
	print '\tPrecision at 10: ' + str(calcPrecRecallAtK(query, 10, lines)['precision'])
	
	ranking = getRankingForQuery(query, 5, lines)
	ranking5 = getRankingForQuery(query, 5, lines)
	ranking10 = getRankingForQuery(query, 10, lines)
	
	#averate NDCG for 5 rankings and 10 rankings
	avg = ndcg_at_k(ranking5, 5)
	avg += ndcg_at_k(ranking10, 10)
	avg = avg/float(2)
	print '\taverage NDCG: ' + str(avg)

	rPrecision += r_precision(ranking)

	
	print ''

MAP = MAP/float(64)
print 'MAP: ' + str(MAP)


rPrecision = rPrecision/float(64)
print 'R-Precision: ' + str(rPrecision)


'''
masterPntCol = []
for i in range(1, 65):
	res = genPrecRecallGraph(i, 5, lines)
	
	if( len(res) > 0 ):
		masterPntCol.append( res )	
plotOriginalPoints(masterPntCol)
'''


