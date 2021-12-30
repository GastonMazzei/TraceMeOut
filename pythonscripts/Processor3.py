import re, json, sys, pickle, yaml, os, linecache, time
import numpy as np
import configuration as config
import pandas as pd
from aux import update_config
from parser import parse_wrapper, show
 
def indexer_evolver(v,DT,L, t0_start=False):
	if t0_start == False:
		i = 0
		t0 = v[0]
	else:
		t0 = t0_start
		## Look for the i so that v[i]-t0_start is minimum only if v[i]-t0 is positive
		searchMe = np.where(v>=v0_start,v-t0_start,np.inf)
		i = np.argmin(searchMe)
	j = i + 1
	tf  = t0
	powers = [2**q for q in range(22)]
	pMix = len(powers)-1
	lapcounter = 0
	while j<L:
		lapcounter += 1
		Nwithout = 0
		# Strategy for exploring exponentially what is the range of the 'latest tree'
		while v[j]-t0<DT:
			newj = j + powers[Nwithout]
			if newj<L:
				if v[newj]-t0<DT:
					Nwithout += 1
					j = newj
					continue
			if Nwithout == 0:
				j = newj
				break
			else:
				Nwithout -= 1
		tf = v[j-1]
		if  lapcounter%250==0: print(f'Processed {j} of {L}')
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

def clean_data(a):
	"""
	Keeps the last relevant info of an array, from the first index False onwards
	e.g. [(False,data1),(True,data2),(True,data3),(False,data4),(True,data5)]
	is converted to
	[(False,data4),(True,data5)]
	"""
	ix_last_false = len(a)-1
	while ix_last_false>0:
		if not a[ix_last_false][0]:
			del(a[:ix_last_false])
			break
		else:
			ix_last_false -= 1
	return

if __name__ == '__main__':
	with open('helpers/unique_elems.pkl','rb') as f:
		G = pickle.load(f)
	def tagger(nm):
		try:
			return G[nm]
		except:
			if nm not in G.keys():
				G['!__COUNTER__!'] += 1
				G[nm] = G['!__COUNTER__!']
		return G[nm]

	VERBOSE = [True, False][1]
	df = pd.read_csv('helpers/categories.csv')
	df_categories = df.iloc[:,0].to_numpy()
	NCATEGORIES = max(df.iloc[:,0])+1
	update_config({'NCATEGORIES':NCATEGORIES})
	def get_t0:
		min_so_far = np.inf
		for N in config.PROCS:
			FILENAME_TIME = f'processed_trace/Processor{N}Times.txt'
			with open(FILENAME_TIME, 'r') as f:
				times = json.load(f)
			times = np.asarray(times)
			if min(times)<min_so_far:
				min_so_far = min(times)
		return min_so_far
	def main(N,df, T0starter):
		df_uptimes = df[f"TimeProc{N}"].to_numpy()
		FILENAME = f'processed_trace/PostProcessed{N}Trace.txt'
		FILENAME_TIME = f'processed_trace/Processor{N}Times.txt'
		
		# Open time
		with open(FILENAME_TIME, 'r') as f:
			times = json.load(f)
		times = np.asarray(times)
		if VERBOSE: print(f'median wait between calls and std are: {round(np.mean(np.diff(times)),3)}us {round(np.std(np.diff(times)),2)}us')
		

		# Compute the checkmarks
		with open(FILENAME, 'r') as f:
			data = f.readlines()
		CHECKMARKS = []
		for i,x in enumerate(data):
			if x[0]=='-':
				CHECKMARKS.append(i)
		CHECKMARKS = np.asarray(CHECKMARKS)
		print(f'for Proc {N}: mean duration for each tree in microseconds (us) is {1e6 * np.mean(np.diff([times[c] for c in CHECKMARKS]))}, while DT (in us) is currently {config.dt}')

		# Compute the portions that have to be considered
		data_generator  = indexer_evolver(times, config.dt/1e6, len(times), T0starter)
		answer, firstLap = True, True
		FIRSTLINE, PREV_LASTLINE, LASTLINE, PREV_FIRSTLINE = 0,0,0,0
		data  = []
		X1,X2,Y = [],[],[]
		cter = 0
		while answer != None:
			if cter % 5 == 0: clean_data(data)
			answer = data_generator.__next__()
			if answer != None:	
				i_,IX,t0_,tf_ = answer
			else:
				break
			if df_categories[closer_nonnegative(df_uptimes, tf_)]==-1:
				# Skip this lap as it has no target to classify, i.e. it is data from the beggining
				# when users werent yet able to mark which tag belonged to their then current activity
				#print('continuing',tf_);import time; time.sleep(0.01)
				continue
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
			cter += 1

			# Save!
		with open(f'processed_trace/Dataset{N}.pkl','wb') as f:
			pickle.dump({'X1':X1,'X2':X2,'Y':Y}, f)

	global_t0 = get_t0()
	# Wrapping the previous operations inside the function Main allows us to enjoy memory descoping :-) so the space is reduced ~ by 4
	for N in config.PROCS: # Variable defined in the configuration file
		main(N, df, global_t0)








