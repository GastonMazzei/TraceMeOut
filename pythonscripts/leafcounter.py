
import re, json, sys, pickle, yaml
import numpy as np
from collections import deque

def leafcounter_list(o):
	c = 0
	for x in o:
		if type(x) == str:
			c += 1
		elif type(x) == list:
			c += leafcounter_list(x)
		elif type(x) == dict:
			c += leafcounter(x)
	return c


def leafcounter(d):
	if type(d) == dict:
		c = len(d.keys())
		for k in d.keys():
			if type(d[k]) == dict:
				c += leafcounter(d[k])
			elif type(d[k]) == list:
				c += leafcounter_list(d[k])
			elif type(d[k]) == str:
				c += 1
	elif type(d) == str:
		c = 1
	elif type(d) == list:
		c = leafcounter_list(d)
	return c
