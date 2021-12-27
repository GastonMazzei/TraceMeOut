

import pickle


import matplotlib.pyplot as plt
import numpy as np

import configuration as config

# Compute the maximum size of the system :0
VERBOSE = [True,False][1]
ML = 0
MI = 0
for P in config.PROCS:
	with open(f'processed_trace/Dataset{P}.pkl','rb') as f:
		data = pickle.load(f)
	lens = [len(x) for x in data['X1']]
	ML = max([ML, max(lens)])
	if  VERBOSE: plt.hist(lens);plt.show()
	for i in range(len(data['X2'])):
		lc = 0
		ks = list(data['X2'][i].keys())
		K = max(ks)  if ks!=[] else 0
		local = []
		for k_ in range(K):
			lc += len(data['X2'][i].get(k_,[]))
			local.append(data['X2'][i].get(k_,[]))
		data['X2'][i] = local.copy()
		MI = max([MI, lc])
	with open(f'processed_trace/Dataset{P}.pkl','wb') as f:
		pickle.dump(data,f)

# Update the values of the configuration file :-)
with open('configuration.py','r') as f:
	cfile = f.readlines()
with  open('helpers/unique_elems.pkl','rb') as f:
	uniques = pickle.load(f)
UNIQUES = len(uniques.keys())-1
for i in range(len(cfile)):
	if 'ML' in cfile[i]:
		cfile[i] = f'ML={ML} ' + ((' #' + cfile[i].split('#')[1][:-1]) if len(cfile[i].split('#'))>1 else '') +'\n'
		print(f'Updated max length to {ML}')
	if 'MI' in cfile[i]:
		cfile[i] = f'MI={MI} ' + ((' #' + cfile[i].split('#')[1][:-1]) if len(cfile[i].split('#'))>1 else '') +'\n'
		print(f'Updated max interaction to {MI}')
	if 'UNIQUES' in cfile[i]:
		cfile[i] = f'UNIQUES={UNIQUES} ' + ((' #' + cfile[i].split('#')[1][:-1]) if len(cfile[i].split('#'))>1 else '') +'\n'
		print(f'Updated Nuniques to {UNIQUES}')
with open('configuration.py','w') as f:
	for x in cfile:
		f.write(x)


