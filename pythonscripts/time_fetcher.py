import subprocess
import time
import signal
import sys
import pandas as pd

VERBOSE = [True,False][0]
category = []

CtrlC_MSG = '[WARNING] by exiting with Ctrl+C you have left the tracer ON! To fix this just \'echo "nop" > /sys/kernel/debug/tracing/current_tracer\', perhaps from sudo. Else your computer will be dealing with some considerable overhead, and it may not go away with a simple reset! :o'

def signal_handler(signal, frame):
	global category
	if VERBOSE: print(f'Ctrl+C received. Exiting gracefully! :-)')
	#uptime = float(subprocess.check_output("cat /proc/uptime", shell=True).decode('utf8').split(' ')[0])*1e6
	#ctime = float(time.time())*1e6
	#category += [(-1,uptime,ctime)]
	a,b,c = zip(*category)
	df = pd.DataFrame({"category":a, "uptime (us)":b, "epochtime (us)":c})
	df.to_csv('helpers/categories.csv',index=False)
	if VERBOSE: print(df.head())
	for _ in range(100): 
		print(CtrlC_MSG)
	sys.exit(0)

# Beggining
uptime = float(subprocess.check_output("cat /proc/uptime", shell=True).decode('utf8').split(' ')[0])*1e6
ctime = float(time.time())*1e6
category += [(-1,uptime,ctime)]

# Signal handler for exit :-)
signal.signal(signal.SIGINT, signal_handler)

# Core
while True:
	answer = input("Hello, please input a number between 0 and N-1 to record the beggining of one of N possible activities :-).\n(To exit type  'exit'!)\nYour answer: ")
	if answer=='exit': break
	uptime = float(subprocess.check_output("cat /proc/uptime", shell=True).decode('utf8').split(' ')[0])*1e6
	ctime = float(time.time())*1e6
	category += [(int(answer),uptime,ctime)]

a,b,c = zip(*category)
df = pd.DataFrame({"category":a, "uptime (us)":b, "epochtime (us)":c})
df.to_csv('helpers/categories.csv',index=False)

