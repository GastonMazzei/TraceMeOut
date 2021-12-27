


import re, json, sys, pickle, yaml
import numpy as np
from collections import deque
from configuration import ML, dt


def update_config(data):
	with open('configuration.py','r') as f:
		config = f.readlines()
	PEND = len(data.keys())
	for i in range(len(config)):
		if PEND == 0: break
		for k in data.keys():
			if k in config[i]:
				config[i] = f'{k}={data[k]}\n'
				PEND -= 1
	with open('configuration.py','w') as f:
		for x in config:
			f.write(x)
			






def elem_mapper_builder(data):

	def leafcounter(d, ids):
		if type(d) == dict:
			c = len(d.keys())
			for k in d.keys():
				incorporate(k,ids)
				if type(d[k]) == dict:
					c += leafcounter(d[k])
				elif type(d[k]) == list:
					c += leafcounter_list(d[k], ids)
				elif type(d[k]) == str:
					c += 1
					incorporate(d[k],ids)
		elif type(d) == str:
			c = 1
			incorporate(d,ids)
		elif type(d) == list:
			c = leafcounter_list(d, ids)
		return c



	def leafcounter_list(o, ids):
		c = 0
		for x in o:
			if type(x) == str:
				c += 1
				incorporate(x, ids)
			elif type(x) == list:
				c += leafcounter_list(x, ids)
			elif type(x) == dict:
				c += leafcounter(x, ids)
		return c


	def depth(d):
		queue = deque([(id(d), d, 1)])
		memo = set()
		while queue:
			id_, o, level = queue.popleft()
			if id_ in memo:
				continue
			memo.add(id_)
			if isinstance(o, dict):
				queue += ((id(v), v, level + 1) for v in o.values())
		return level

	def incorporate(s,v):
		increase_global_log(s)
		v.append(GLOBAL_LOG[s])



	def increase_global_log(k):
		if k not in GLOBAL_LOG.keys():
			GLOBAL_LOG['!__COUNTER__!'] += 1
			GLOBAL_LOG[k] = GLOBAL_LOG['!__COUNTER__!']


	try:
		with open('helpers/unique_elems.pkl','rb') as f:
			GLOBAL_LOG = pickle.load(f)
	except:
		GLOBAL_LOG = {'!__COUNTER__!':0}
	
	
	maximum_leaves = 0
	if type(data)==list:
		for x in data:
			vector_temp = []
			local_count = leafcounter(x,vector_temp)
			if local_count > maximum_leaves:
				maximum_leaves = local_count
	elif type(data) == dict:
		maximum_leaves = local_count
		
	with open('helpers/unique_elems.pkl','wb') as f:
		pickle.dump(GLOBAL_LOG, f)

	return maximum_leaves
