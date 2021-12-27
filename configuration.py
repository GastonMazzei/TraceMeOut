
# Model-specific parameters
T=8 # duration of the window in dt units
dt = 100 # time in microseconds
UNIQUES=1576  #number of unique ids
MI=14864  #max number of interactions
ML=14866  #max number of leaves
NCATEGORIES=2

# Architectural parameters
ACT1 = 'relu'
FILTERS1 = 8
KSIZE1 = (2,1)
NDENSE1 = 16

ACT2 = 'relu'
FILTERS2 = 8
KSIZE2 = (2,2)
stride = (1,1)
NDENSE2 = 16

ACT3='relu'
NDENSE3=8

# Training parameters
VAL=0.3
BATCH=4
EPOCHS=3

# Extras
POOLING = False
PROCS=[3, 2, 0, 1]
