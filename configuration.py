
# Model-specific parameters
T=8 # duration of the window in dt units
dt = 4000 # time in microseconds
UNIQUES=3807  #number of unique ids
MI=4762  #max number of interactions
ML=4765  #max number of leaves
NCATEGORIES=2

# Architectural parameters
ACT1 = 'relu'
FILTERS1 = 8
KSIZE1 = (2,1)
PSIZE1 = (max([T//4,2]),)
NDENSE1 = 16
DROP1 = 0.4

ACT2 = 'relu'
FILTERS2 = 8
KSIZE2 = (2,2)
PSIZE2 = (max([T//2,2]),1)
stride = (1,1)
NDENSE2 = 16
DROP2 = 0.75


ACT4='relu'
NDENSE4=8
DROP4 = 0.2


ACT3='relu'
NDENSE3=8
DROP3 = 0.4


# Training parameters
VAL=0.25
BATCH=10
EPOCHS=50
L=5 # a length used to generate random data just for testing
LR=0.05



# Extras
POOLING = False
PROCS=[3, 2, 0, 1]
