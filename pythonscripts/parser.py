import yaml



def tagger(nm):
    return 125

def parse_wrapper(data, ixs,conns,tagf):
    parse(data,ixs,conns,-1, tagf)
    del conns[-1]

def parse(data,ixs,conns,i, tagger):
    if type(data)==list:
        for x in data:
            parse(x,ixs,conns,i, tagger)
    if type(data)==str:
        my_name = tagger(data)
        ixs.append(my_name)
        my_ix = len(ixs)-1
        conns[i] = conns.get(i,[]) + [my_ix]
    if type(data)==dict:
        for k in data.keys():
            # consume and connect the keys
            parse(k,ixs,conns,i, tagger)
            # also take care of the object that the key references
            parse(data[k],ixs,conns,len(ixs)-1, tagger) # the index is that of the key just added


def show(conns):
    for k,v in conns.items():
        print(k,v)

if __name__=='__main__':
    with open('eg','r') as f:
        d = yaml.safe_load(f)
    with open('eg','r') as f:
        dl = f.readlines()
    # Parse
    ixs = []
    conns = {}
    parse_wrapper(d,ixs,conns,tagger)
    # Print
    print(''.join(dl))
    print(ixs)
    show(conns)

