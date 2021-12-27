import pickle, sys, os

import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt
from aux_networkx import hierarchy_pos

with open('processed_trace/Dataset0.pkl','rb') as f:
	d = pickle.load(f)


def build_adj_matr(v):
	L = 1 + max([len(v), max([max(x) if x!=[] else -1 for x in v])])
	am = np.zeros((L,L))
	print(am.shape,L)
	return 

i = -1
NO_STRUCTURE = [True, False][0]
while True:
	i += 1
	G = nx.from_numpy_matrix(build_adj_matr(d['X2'][i]))  
	if NO_STRUCTURE:
		nx.draw(G, with_labels=True) 
	else:
		pos = hierarchy_pos(G,0) 
		nx.draw(G, pos=pos, with_labels=True)
	plt.show()
