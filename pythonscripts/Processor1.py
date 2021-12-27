import os, json, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Open file
with open('raw_data/trace','r') as f:
	d = f.readlines()

# Splitting data per processor
split = {0:[]}
times = {}
PMax = 0
errors = 0
for  _ in d:
	try:
		PLocal = int(_.split('|')[1].split(')')[0])
		if PLocal > PMax:
			PMax = PLocal
		if PLocal not in split:
			split[PLocal] = []
		if '|' in _:
			split[PLocal] += [_]
	except Exception as ins:
		errors += 1

for k in split.keys():
	times[k] = []

# Making the trace start from a non-nested operation
for k in split.keys():
	cropping_indexes = []
	for i,x in enumerate(split[k]):
		local_x = '|' + x.split('|')[-1]
		if '#' not in local_x:
			f = re.findall('\|([\s]*)',local_x)
			assert(len(f)<=1)
			if len(f)==1:
				if len(f[0])==2:
					cropping_indexes.append(i)
	print(len(cropping_indexes))
	min_start = -1
	if '}' in split[k][cropping_indexes[0]]:
		min_start = cropping_indexes[1]
	else:
		min_start = cropping_indexes[0]
	if '}' in split[k][cropping_indexes[-1]]:
		max_end = cropping_indexes[-1]
	else:
		if '}' in split[k][cropping_indexes[-2]]:
			max_end = cropping_indexes[-2]
		else:
			if '}' in split[k][cropping_indexes[-3]]:
				max_end = cropping_indexes[-3]
			else:
				print(split[k][cropping_indexes[-1]], split[k][cropping_indexes[-2]], split[k][cropping_indexes[-3]])
				raise Exception("Incoherent structure! information is probably missing.")
	split[k] = split[k][min_start:max_end]
	# Here it is where  the splits are  separated :-)
	for i in range(len(split[k])):
		try:
			times[k].append(str(float(split[k][i].split('|')[0])))
			split[k][i] = split[k][i].split('|')[-1]
		except:
			print("Fatal error!", len(_.split('|')[-1]))
			
# Mini report
print("Mini report:")
print(f"Processing errors: {errors} out of {len(d)} ({round(100*errors/len(d),3)}%) \n(some are acceptable because of comments and headers)")
print(f'NProcessors detected: {1+PMax}')


# Postprocessing
#
# data is:
#
# n)  time  | 8 white spaces and information
for N in split.keys():
	result = ''.join(split[N][:])
	with open(f'processed_trace/Processor{N}Trace.txt','w') as f:
		f.write(result)
	result = ','.join(times[N][:])
	with open(f'processed_trace/Processor{N}Times.txt','w') as f:
		f.write(result)
