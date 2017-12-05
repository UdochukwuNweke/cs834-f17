from sklearn.cluster import KMeans
import numpy as np
from spherecluster import SphericalKMeans

X = np.array([[-4, -2], [-3, -2], [-2, -2], [-1, -2], 
	[1, -1], [1, 1], [2, 3], [3, 2], [3, 4], [4, 3]])


def testKMeans():
	kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
	print( kmeans.labels_ )
	#print( kmeans.predict([[0, 0], [4, 4]]) )

def testSpericalKMeans():
	# Find K clusters from data matrix X (n_examples x n_features)
	# spherical k-means

	skm = SphericalKMeans(n_clusters=3)
	skm.fit(X)
	print( skm.labels_ )

testKMeans()
testSpericalKMeans()