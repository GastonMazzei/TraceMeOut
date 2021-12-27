import re, json, sys, pickle, yaml, os, linecache, time
import numpy as np
import configuration as config
import pandas as pd
from aux import update_config
from parser import parse_wrapper, show
 
def indexer_evolver(v,DT,L):
	i = 0
	j = 1
	t0 = v[i]
	tf  = t0
	while j<L:
		while v[j]-t0<DT:
			j+=1
			if j>=L: break
		tf = v[j-1]
		yield i,j,t0,tf
		t0 += DT
		i = j-1
	yield None

def closer_nonnegative(v,y):
	return np.argmax(np.where(y >= v, v-y, -np.inf))

def build_data(d):
    total = d[-1][1]
    i = len(d)-1
    try:
        while d[i][0]:
            total = d[i-1][1] + total
            i -= 1
            if i<1: break
        if total=='': raise Exception('empty!')
        return yaml.safe_load(total)
    except Exception as ins:
        print('ERROR!')
        print(len(d))
        print(i, [dx[0] for dx in d])
        os.system(f'echo "{total}" > temp.log')
        print(ins.args)
        sys.exit(1)

if __name__ == '__main__':
	with open('helpers/unique_elems.pkl','rb') as f:
		G = pickle.load(f)
	def tagger(nm):
		return G[nm]
	VERBOSE = [True, False][1]
	df = pd.read_csv('helpers/categories.csv')
	df_uptimes = df.iloc[:,1].to_numpy()
	df_categories = df.iloc[:,0].to_numpy()
	NCATEGORIES = max(df.iloc[:,0])+1
	update_config({'NCATEGORIES':NCATEGORIES})
	for N in config.PROCS: # Variable defined in the configuration file
		FILENAME = f'processed_trace/PostProcessed{N}Trace.txt'
		FILENAME_TIME = f'processed_trace/Processor{N}Times.txt'
		
		# Open time
		with open(FILENAME_TIME, 'r') as f:
			times = json.load(f)
		times = np.asarray(times)* 1e6
		if VERBOSE: print(f'median wait between calls and std are: {round(np.mean(np.diff(times)),3)}us {round(np.std(np.diff(times)),2)}us')
		

		# Compute the checkmarks
		with open(FILENAME, 'r') as f:
			data = f.readlines()
		CHECKMARKS = []
		for i,x in enumerate(data):
			if x[0]=='-':
				CHECKMARKS.append(i)
		CHECKMARKS = np.asarray(CHECKMARKS)

		# Compute the portions that have to be considered
		data_generator  = indexer_evolver(times, config.dt, len(times))
		answer, firstLap = True, True
		FIRSTLINE, PREV_LASTLINE, LASTLINE, PREV_FIRSTLINE = 0,0,0,0
		data  = []
		X1,X2,Y = [],[],[]
		cter = 0
		while answer != None:
			answer = data_generator.__next__()
			if answer != None:	
				i_,IX,t0_,tf_ = answer
			else:
				break
			if VERBOSE: print(f't0,tf = {t0_} {tf_}')
			if VERBOSE: time.sleep(2)
			# Open the file selectively ;-)
			PREV_FIRSTLINE = FIRSTLINE
			FIRSTLINE = CHECKMARKS[closer_nonnegative(CHECKMARKS, IX)]
			PREV_LASTLINE = LASTLINE
			LASTLINE = IX
			if FIRSTLINE==LASTLINE: LASTLINE += 1
			localdata = []
			if PREV_FIRSTLINE != FIRSTLINE:
				for i in range(FIRSTLINE, LASTLINE):
					localdata += [linecache.getline(FILENAME, i+1)]
				data += [(False, ''.join(localdata))]
			else:
				for i in range(PREV_LASTLINE, LASTLINE):
					localdata += [linecache.getline(FILENAME, i+1)]
				data += [(True, ''.join(localdata))]
			if VERBOSE: print([dx[0] for dx in data])
			

                        # Build Y: we use the category closer to the end, i.e. tf_ 
			Y.append(df_categories[closer_nonnegative(df_uptimes, tf_)])
			if VERBOSE: print(f'Latest category is: {Y[-1]}, prev_firstline={PREV_FIRSTLINE}, firstline={FIRSTLINE}, last&prevlast={LASTLINE},{PREV_LASTLINE}')


			# Build X1 and X2: we must build a graph using data[-1] to data[..-N] until the first item is True (included)
			ixs, cons = [],{}
			dic = build_data(data)
			
			parse_wrapper(dic,ixs,cons,tagger)
			X1 += [ixs.copy()]
			X2 += [cons.copy()]

			# Save!
			with open(f'processed_trace/Dataset{N}.pkl','wb') as f:
				pickle.dump({'X1':X1,'X2':X2,'Y':Y}, f)












