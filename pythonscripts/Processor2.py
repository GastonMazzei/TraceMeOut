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
		print('About to run Main for n:',n)
		main(n)
		print("About to unnest...")
		unNest_once(n)


	sys.exit(1)
