import subprocess
import time
import signal
import sys
import os
import pandas as pd
import linecache 

# Record the initial time and compute the offset in each processor
MAXCORES = 20
t0 = time.time()
OFFSET = [0 for _ in range(MAXCORES)]
time.sleep(0.5)
ALL_INFO_FILES = [x for x in os.listdir('.') if '.info' in x]
for infoFile in ALL_INFO_FILES:
	ix = int(infoFile.split('cpu')[1].split('.')[0])
	with open(infoFile, 'r') as f:
		for x in f.readlines():
			if 'now ts' in x:
				OFFSET[ix] = float(x.split(' ')[-1][:-1])
				break


# Define container and error message
VERBOSE = [True,False][0]
category = []
CtrlC_MSG = '\n\n\n\n[WARNING] by exiting with Ctrl+C you may have left the tracer ON! To fix this just \'echo "nop" > /sys/kernel/debug/tracing/current_tracer\', perhaps from sudo. Else your computer will be dealing with some considerable overhead, and it may even not go away with a simple reset! :o Also the kernel trace pipe could not have been successfully turned off, so a file is being written at approx 1Gb/min rate. This is DANGEROUS, it goes away if the tracer is turned off but it also goes away with a RESET. The file to erase after this will be raw_data/trace :-)\n\n\n\n'

# Define two useful functions
def get_uptime():
	tnow = 	time.time()
	global t0
	return tnow-t0
	
def signal_handler(signal, frame):
	global category
	if VERBOSE: print(f'Ctrl+C received. Exiting gracefully! :-)')
	X = list(zip(*category))
	df = pd.DataFrame({"category":X[0], **{f"TimeProc{n}":X[n+1] for n in range(MAXCORES)}})
	if VERBOSE: print(df.head())
	# If Ctrl+C was sent, say a hundred times that the kernel tracer could still be on
	for _ in range(100): 
		print(CtrlC_MSG)
	sys.exit(0)

# Beggining
tnow = get_uptime()
category += [(-1,*[OFFSET[i] + tnow for i in range(MAXCORES)])]

# Signal handler for Ctrl+C catch exit :-)
signal.signal(signal.SIGINT, signal_handler)

# Main Section
while True:
	answer = input("Hello, please input a number between 0 and N-1 to record the beggining of one of N possible activities :-).\n(To exit type  'exit'!)\nYour answer: ")
	if answer=='exit': break
	tnow = get_uptime()
	category += [(int(answer),*[OFFSET[i] + tnow for i in range(MAXCORES)])]

# Graceful exit goes here :-)
X = list(zip(*category))
df = pd.DataFrame({"category":X[0], **{f"TimeProc{n}":X[n+1] for n in range(MAXCORES)}})
df.to_csv('helpers/categories.csv',index=False)





















