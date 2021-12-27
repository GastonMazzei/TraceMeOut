import os, sys, pickle, json, re
from functools import reduce  
import matplotlib.pyplot as plt
import numpy as np
import operator

#OBS: in blue what should be the C++ implementation :-)

NAME = sys.argv[1]

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

def parse(total, i, nest, result, j, unique_elems):
	if len(total) == i: return i+1, nest, j
	# Path 1) it's a comment and some closing
	if '/*' in total[i] and '*/' in total[i]:
		if '}' in total[i]:
			nest -= 1
		if len(j)>1:
			j = j[:-1]
		#parse(total, i+1, nest, result, j, unique_elems)
		return i+1, nest, j
	# Path 2) it's only a closing thing
	elif '}' in total[i]:
		nest -= 1
		if nest == 0:
			result += [{}]
			j = [j[0]+1]
		else:
			if len(j)>1:
				j = j[:-1]	
		return i+1, nest, j
		#parse(total, i+1, nest, result, j, unique_elems)

	# Path 3) it's an opening
	elif '{' in total[i]:
		nest += 1
		localdata = total[i].split('()')[0].split(' ')[-1]
		unique_elems.add(localdata)
		update_item_and_expand(j[1:], result[j[0]], localdata)
		j.append(localdata)
		#parse(total, i+1, nest, result, j, unique_elems)
		return i+1, nest, j	

	# Path 4) it's a call that  ends  with ; without affecting nesting
	elif ';' in total[i]:
		localdata = total[i].split('()')[0].split(' ')[-1]
		unique_elems.add(localdata)
		update_item_and_expand(j[1:], result[j[0]], localdata)
		if nest == 0 and len(j)==1:
			j = [j[0]+1]
			result += [{}]
		#parse(total, i+1, nest, result, j, unique_elems)	
		return i+1, nest, j
	return i+1, nest, j

def update_item_and_expand(j, result, localdata):
	if j==[]:
		result[localdata]={}
	elif len(j)>=1:
		setInDict(result, j+[localdata],{})
#	elif len(j)==1:
#		result[j[0]][localdata] = {}
#	elif len(j)>1:
#		update_item_and_expand(j[1:], result[j[0]], localdata)	
	else:
		print("[ERROR] [update_item_and_expand] Fatal unknown (bad design?)")
		sys.exit(1)










unique_elems = set()
result = [{}]
j=[0]
nest = 0
i=0
with open(NAME+'.txt','r') as f:
	total = f.readlines()
with open(NAME[:-5]+'Times.txt','r') as f:
	times = f.readlines()
assert(len(times) == 1)
times = [float(x) for x in times[0].split(',')]

# main function
counter = 0
relevant_times = []
rt1, rt2 = times[0],0
rL = 0
assert(len(times) == len(total))
while i<len(total):
	try:
		if len(result) != rL:
			rL = len(result)
			rt2 = times[i-1]
			relevant_times.append((rt1,rt2))
			rt1 = times[i]
		i, nest, j = parse(total, i, nest, result, j, unique_elems)
	except Exception as ins:
		print(ins.args)
		print(j)
	counter += 1
assert(len(relevant_times) == len(result))

print(f'counter was: {counter}, len of total was: {len(total)}')

WATCH_RESULT = [True, False][1]
WATCH_UNIQUES = [True, False][1]
WATCH_NUMBER_UNIQUES = [True, False][0]

if WATCH_RESULT:
	delim="\n-------------\n"
	print(f"{delim}RAW{delim}")
	for t in total:
		print(t)
	print(f"{delim}PROCESSED{delim}")
	for x in result:
		for k in x.keys():
			print(k)
			for k2 in x[k].keys():
				print(f'\t{k2}')
				print(f'\t\t{x[k][k2]}')

if WATCH_UNIQUES:
	print(unique_elems)	

if WATCH_NUMBER_UNIQUES:
    print(f'Number of total different functions called: {len(unique_elems)}')

with open(NAME+'.json', 'w') as f:
	json.dump(result, f)

# FurtherReducingTimes
with open(NAME[:-5]+'Times.json','w') as f:
	json.dump(relevant_times, f)


# Update the dt configuration
from configuration import dt
characteristic_time = 1e6 * np.mean(np.diff(relevant_times,1))
print(characteristic_time)
if dt > characteristic_time:
	with open('configuration.py','r') as f:
		conf = f.readlines()
	for il,l in enumerate(conf):
		if 'dt' in l:
			a = re.findall('([0-9\.]+)',l)[0]
			b = l.split(a)
			c = f'{characteristic_time}'.join(b)
			conf[il] = c
       





