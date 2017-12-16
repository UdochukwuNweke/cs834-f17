import matplotlib.pyplot as plt
import networkx as nx

def runPageRank(G):
	pr = nx.pagerank(G)
	#iter: 5
	#{1: 0.12066620697948402, 2: 0.22304902340308913, 3: 0.09418933961948064, 4: 0.2795274111395043, 5: 0.09418933961948064, 6: 0.09418933961948064, 7: 0.09418933961948064}
4, 2, 1, (3, 5, 6, 7 - tied)

def runHITS(G):
	h, a = nx.hits(G)
	print 'h:', h
	print 'a:', a

	#iter: 5
	#pre h: {1: 0.310838445807771, 2: 0.0, 3: 0.9999999999999999, 4: 0.0, 5: 0.45194274028629855, 6: 0.45194274028629855, 7: 0.0}
	#pre a: {1: 0.5248868778280543, 2: 0.6877828054298643, 3: 0.0, 4: 0.9999999999999999, 5: 0.0, 6: 0.0, 7: 0.0}
4, 2, 1, (3,5,6,7 - tied)



G = nx.DiGraph()
G.add_node(7)
G.add_edge(1, 2)
G.add_edge(3, 1)
G.add_edge(3, 2)
G.add_edge(3, 4)
G.add_edge(5, 4)
G.add_edge(6, 4)

runHITS(G)
#runPageRank(G)


#nx.draw(G)
#plt.savefig('graph.png')