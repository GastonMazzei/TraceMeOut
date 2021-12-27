import yaml, json


def main(N):
    newtimes = []
    FILENAME_TIME = f'processed_trace/Processor{N}Times.txt'
    with open(FILENAME_TIME, 'r') as f:
        times = [float(x) for x in f.readlines()[0].split(',')]
    with open(f'processed_trace/Processor{N}Trace.txt','r') as f:
        q = f.readlines()
    assert(len(times) == len(q))
    counts = []
    new = []
    c = 0
    unwanted = [';','()','{','}']
    for i in range(len(q)):
        if '}' in q[i]:
            continue
        new += [q[i]]
        newtimes += [times[i]]
        for u in unwanted:
            if u in new[c]:
                new[c] = new[c].replace(u,'')
        new[c] = new[c][:-1]
        if len(new[c])>0:
            j = len(new[c])-1
            while new[c][j] == ' ':
                j -= 1
                new[c] = new[c][:-1]
            s = new[c].split(' ')
            counts.append(1)
            for si in range(1,len(s)):
                if s[si]=='' and s[si-1]=='':
                    counts[-1]+=1
            new[c] = ''.join(s)
            c += 1
        else:
            del new[-1]
            del newtimes[-1]
    JK = '.'
    m = min(counts)
    counts = [x-m for x in counts]
    for i in range(1,len(counts)):
        if counts[i]>counts[i-1]:
            counts[i] = counts[i-1]+2
        elif counts[i]<counts[i-1]:
            counts[i] = counts[i-1]-2

    new = [x.replace('.',JK).replace('_',JK).replace('[','').replace(']','') for i,x in enumerate(new)]
    for i in range(len(new)):
        new[i]= ' '*counts[i] + "- " + new[i] + " :\n"

    for i in range(len(new)-1):
        if counts[i+1]<=counts[i]:
            new[i] = new[i].replace(':','')

    with open(f'processed_trace/PostProcessed{N}Trace.txt','w') as f:
        for x in new:
            f.write(x)
    with open(FILENAME_TIME, 'w') as f:
        json.dump(newtimes,f)
    TEST = [True, False][1]
    if TEST:
        import yaml
        with open(f'processed_trace/PostProcessed{N}Trace.txt','r') as f:
            d = yaml.safe_load(f)
        print('The yaml file can be sucessfully read, and its length is: ',len(d))
        print(f'Keys for each are: {[item.keys() if "keys" in dir(item) else item for item in d]}')

def unNest_once(n):
	with open(f'processed_trace/PostProcessed{n}Trace.txt','r') as f:
		d = f.readlines()
	with open(f'processed_trace/PostProcessed{n}Trace.txt','w') as f:
		for x in d:
			if x[0]==' ':
				f.write(x[2:])


if __name__ == '__main__':
	main(0)
