# -*- coding: utf-8 -*-
from scipy import cluster
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt
import numpy as np

def clustering():
	#https://stackoverflow.com/a/21723473
	a = np.array([[-4, -2], [-3, -2], [-2, -2], [-1, -2], [1, -1], [1, 1], [2, 3], [3, 2], [3, 4], [4, 3]])

	fig, axes23 = plt.subplots(2, 3)

	for method, axes in zip(['ward'], axes23):
		z = hac.linkage(a, method=method)

		# Plotting
		axes[0].plot(range(1, len(z)+1), z[::-1, 2])
		knee = np.diff(z[::-1, 2], 2)
		axes[0].plot(range(2, len(z)), knee)

		num_clust1 = knee.argmax() + 2
		knee[knee.argmax()] = 0
		num_clust2 = knee.argmax() + 2


		#axes[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')
		print 'num_clust1:', num_clust1
		print 'num_clust2:', num_clust2
		#num_clust1 = 3
		part1 = hac.fcluster(z, num_clust1, 'maxclust')
		part2 = hac.fcluster(z, num_clust2, 'maxclust')
		print('part1:', part1)
		print('part2:', part2)
		


		clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
		'#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']

		for part, ax in zip([part1, part2], axes[1:]):
			for cluster in set(part):
				ax.scatter(a[part == cluster, 0], a[part == cluster, 1], 
						   color=clr[cluster])

		m = '\n(method: {})'.format(method)
		plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition', ylabel='{}\ncluster distance'.format(m))
		
		c0 = len(set(part1.tolist()))
		c1 = len(set(part2.tolist()))

		plt.setp(axes[1], title='{} Clusters'.format(c0))
		plt.setp(axes[2], title='{} Clusters'.format(c1))

		plt.tight_layout()

		plt.savefig('clustering.png')

def plotOriginalPoints():

	fig = plt.figure()
	fig.suptitle('Original data points', fontsize=14, fontweight='bold')

	ax = fig.add_subplot(111)
	fig.subplots_adjust(top=0.85)
	#ax.set_title('axes title')
	ax.set_xlabel('x')
	ax.set_ylabel('y')

	#Original points
	sampMat = [[-4, -2], [-3, -2], [-2, -2], [-1, -2], [1, -1], [1, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
	X = np.array(sampMat)

	#add labels
	for i in range(len(sampMat)):
		ax.text(sampMat[i][0], sampMat[i][1], str(i+1))

	#plot points
	ax.plot(X[:,0], X[:,1], 'o', color='r')

	#set window size
	ax.axis([-5, 6, -3, 6])

	#save plot
	plt.savefig('originalPoints.png')

#plotOriginalPoints()

clustering()