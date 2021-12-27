import re, json, sys, pickle, yaml, os
import numpy as np
from configuration import *

from aux import elem_mapper_builder, update_config 
from trace2yaml import main, unNest_once

if __name__ == '__main__':

	filenames = os.listdir('processed_trace')
	filenames = [x for x in filenames  if 'Processor' in x and 'Trace' in x]
	filenumbers = [int(x.split('Processor')[1].split('Trace')[0]) for x in filenames]
	update_config({'PROCS':filenumbers})
	for n,NAME in [(n,f'PostProcessed{n}Trace') for n in filenumbers]:
		main(n)
		unNest_once(n)
		with open('processed_trace/'+NAME+'.txt','r') as f:
			d = yaml.safe_load(f)

		print(f'The maximum number of leaves for n={n} is: ', elem_mapper_builder(d))


	sys.exit(1)

	# This section could be useful for building the dataset :-)
	with open('processed_trace/'+NAME[:-5]+'Times.json','r') as f:
		t = json.load(f)

	NMAXLEAVES = ML
	uts = []
	ids = []
	newuts = []
	for i in range(len(d)):
		DATA = d[i]
		ids += [[0 for _ in range(NMAXLEAVES+2)]]
		newuts += [[]]
		build_adj2(DATA, ids[-1], i, newuts[-1])

	M = max([len(x) for x in newuts])

	if S>NMAXLEAVES:
		PAD = M - NMAXLEAVES
		padv = [0 for _ in range(len(PAD))]
		for i in range(len(ids)):
			ids[i] = ids[i] + padv
			localL = len(newuts[i])
			if localL < S:
				newuts[i] += [0 for _ in range(S-localL)]	
	uts  = newuts
	
	# Update the configuration file if required :-) and update the unique dict
	Uelems = len(GLOBAL_LOG.keys())-1
	print('...updating the configuration file with thisinformation...')
	with open('configuration.py','r') as f:
		conf = f.readlines()
	for il,l in enumerate(conf):
		if 'MI' in l:
			a = re.findall('([0-9\.]+)',l)[0]
			b = l.split(a)
		if float(a)<M:
			c = f'{M}'.join(b)
			conf[il] = c        
		if 'ML' in l:
			a = re.findall('([0-9\.]+)',l)[0]
			b = l.split(a)
		if float(a)<NMAXLEAVES:
			c = f'{NMAXLEAVES}'.join(b)
			conf[il] = c
		if 'UNIQUES' in l:
			a = re.findall('([0-9\.]+)',l)[0]
			b = l.split(a)
		if float(a)<Uelems:
			c = f'{Uelems}'.join(b)
			conf[il] = c
	with open('configuration.py','w') as f:
		for l in conf:
			f.write(l)
	
	
		# Save the data
	assert(len(t) == len(uts))
	np.save(f'processed_trace/{NAME}-B',uts)
	np.save(f'processed_trace/{NAME}-A',ids)
	
	# Printing the result?
	SHOW_RESULT = [True, False][1]
	PLOTTING = [True, False][1]
	if SHOW_RESULT:
		print(DATA)
		for i,u in enumerate(uts[-1]):
			print(u)
	if PLOTTING:
		import networkx as nx
		import matplotlib.pyplot as plt
		from aux_networkx import hierarchy_pos
		G = nx.DiGraph() 
		for i in range(NMAXLEAVES): 
		 for j in range(NMAXLEAVES): 
		   if uts[-1][i][j] == 1: 
		      G.add_edge(i,j) 
		try:	
			pos = hierarchy_pos(G,0) 
			nx.draw(G, pos=pos, with_labels=True)
			plt.show()
		except:
			nleaves = leafcounter(DATA)	
			for i,u in enumerate(uts[-1][:nleaves]):
				print(u[:nleaves])
			nx.draw(G, with_labels=True)
			plt.show()



# ---------TRASH FUNCTIONS THAT BUILD ADJACENCY MATRICES :P


# Define a function to build the adjacency matrix
def build_adj(d, ut, idl, i, dummyVar=None):
	offsets = [0]
	for k in d.keys():
		increase_global_log(k)
		offsets.append(offsets[-1] + leafcounter(d[k]) + 1)
	for j,k in enumerate(d.keys()):
		ut[i][i+offsets[j]+1] = 1
		idl[i+offsets[j]+1] = GLOBAL_LOG[k]
		if d[k] != {}:
			build_adj(d[k], ut, idl, i+offsets[j]+1)

def replace_adjacency_with_reasonable_encoding(u, i, S, newu):
	newu += [[(0,0) for _ in range(S)]]
	counter = 0
	for j in range(len(u[i])):
		for k in range(len(u[i][j])):
			if u[i][j][k] == 1:
				newu[-1][counter] = (j,k)
				counter += 1


def replace_adjacency_with_reasonable_encoding_locally(u, S, newu):
	newu += [[(0,0) for _ in range(S)]]
	counter = 0
	for j in range(len(u)):
		for k in range(len(u[j])):
			if u[j][k] == 1:
				newu[-1][counter] = (j,k)
				counter += 1


def build_adj2(d, idl, i, newu_elem):
	offsets = [0]
	for k in d.keys():
		increase_global_log(k)
		offsets.append(offsets[-1] + leafcounter(d[k]) + 1)
	for j,k in enumerate(d.keys()):
		newu_elem.append((i,i+offsets[j]+1))
		try: idl[i+offsets[j]+1] = GLOBAL_LOG[k]
		except:
			print(i+offsets[j]+1, len(idl), k in GLOBAL_LOG);sys.exit(1)
		if d[k] != {}:
			build_adj2(d[k], idl, i+offsets[j]+1, newu_elem)






