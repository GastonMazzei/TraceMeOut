import pickle, sys, os

import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt


with open('processed_trace/Dataset0.pkl','rb') as f:
	d = pickle.load(f)

def apply_graphical_path(am):
	deletes  = []
	for i in range(len(am)):
		if 1 not in am[:,i].tolist() and 1 not in am[i,:].tolist():
			deletes.append(i)
	new = []
	for i in range(len(am)):
		if i not in deletes:
			new.append([x for j,x in enumerate(am[i,:].tolist()) if j not in deletes])
	new = np.asarray(new)
	return new
	

def build_adj_matr(v):
	us = set()
	for x in v:
		for y in x: us.add(y)
	L =  1 + max([len(v), max([max(x) if x!=[] else -1 for x in v])])
	am = np.zeros((L,L))

	try:
		for i,x in enumerate(v):
			am[0,i+1] = 1
			for y in x:
				am[i+1,y] = 1
	except Exception as ins:
		print(ins.args)	
		print(x)
		print(i, L, am.shape, y)
		sys.exit(1)
	am = apply_graphical_path(am)
	return am	




lens = [len(x) for x in d['X2']]
print(lens)
i = int(input("In which index should we start? Your answer: "))
c = 1
while True:
	i += 1
	G = nx.from_numpy_matrix(build_adj_matr(d['X2'][i]))  
	nx.draw(G, with_labels=True) 
	plt.show()
	plt.savefig(f'utils/example{c}.png'); c+=1
