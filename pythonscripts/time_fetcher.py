import subprocess
import time
import signal
import sys
import pandas as pd

VERBOSE = [True,False][0]
category = []

def signal_handler(signal, frame):
	global category
	if VERBOSE: print(f'Ctrl+C received. Exiting gracefully! :-)')
	uptime = float(subprocess.check_output("cat /proc/uptime", shell=True).decode('utf8').split(' ')[0])*1e6
	ctime = float(time.time())*1e6
	category += [(-1,uptime,ctime)]	
	a,b,c = zip(*category)
	df = pd.DataFrame({"category":a, "uptime (us)":b, "epochtime (us)":c})
	df.to_csv('helpers/categories.csv',index=False)
	if VERBOSE: print(df.head())
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


