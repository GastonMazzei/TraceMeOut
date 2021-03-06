import pickle,sys,os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from configuration import *

# define two sets of inputs: 
input_shape_flavours = (BATCH, T, ML, 1)
input_shape_structure = (BATCH, T, MI, 2)
inputFlavours = tf.keras.Input(shape=input_shape_flavours[1:])
inputStructure = tf.keras.Input(shape=input_shape_structure[1:])

# the first branch operates on the first input (https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv1D)
x = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS1,         KSIZE1,       (1,1),      'valid',  activation = ACT1,
			input_shape = input_shape_flavours[1:]
			)(inputFlavours)
x = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS1 * 2,         KSIZE1,       (1,1),      'valid',  activation = ACT1,
			)(x)
x = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS1 * 2,         KSIZE1,       (1,1),      'valid',  activation = ACT1,
			)(x)
#x = tf.keras.layers.MaxPool1D(pool_size=PSIZE1)(x)
x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dropout(DROP1)(x)
x = tf.keras.layers.Dense(NDENSE1, activation = ACT1)(x)
x = tf.keras.layers.Dropout(DROP1)(x)
x = tf.keras.layers.Dense(NDENSE1 // 2, activation = ACT1)(x)
x = tf.keras.layers.Dropout(DROP1)(x)
x = tf.keras.layers.Dense(NDENSE1 // 2 // 2, activation = ACT1)(x)
x = tf.keras.Model(inputs = inputFlavours, outputs=x)

# the second branch opreates on the second input (https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)
y = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS2,         KSIZE2,    stride,      'valid',  activation = ACT2,
			input_shape = input_shape_structure[1:]
			)(inputStructure)
y = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS2 * 2,         KSIZE2,       stride,      'valid',  activation = ACT2,
			)(y)
#y = tf.keras.layers.MaxPool2D(pool_size=PSIZE2)(y)
y = tf.keras.layers.Conv2D(
			# Filters, Kersize, Strides, Padding,  Activation
			FILTERS2 * 2,         KSIZE2,       stride,      'valid',  activation = ACT2,
			)(y)
y = tf.keras.layers.MaxPool2D(pool_size=PSIZE2)(y)
y = tf.keras.layers.Flatten()(y)
y = tf.keras.layers.Dropout(DROP2)(y)
y = tf.keras.layers.Dense(NDENSE2, activation = ACT2)(y)
y = tf.keras.layers.Dropout(DROP2)(y)
y = tf.keras.layers.Dense(NDENSE2 // 2, activation = ACT2)(y)
y = tf.keras.layers.Dropout(DROP2)(y)
y = tf.keras.layers.Dense(NDENSE2 // 2 // 2, activation = ACT2)(y)
y = tf.keras.Model(inputs = inputStructure, outputs=y)



# combine the output of the two branches
combined = tf.keras.layers.concatenate([x.output, y.output])
z = tf.keras.layers.Dropout(DROP3)(combined)
z = tf.keras.layers.Dense(NDENSE3, activation = ACT3)(z)
z = tf.keras.layers.Dropout(DROP3)(z)
z = tf.keras.layers.Dense(NDENSE3, activation = ACT3)(z)
z = tf.keras.layers.Dense(NCATEGORIES, activation="softmax")(z)

# our model will accept the inputs of the two branches and
# then output a single value
model = tf.keras.Model(inputs=[x.input, y.input], outputs=z)

# Compile the model :-)
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=1e-3),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalCrossentropy(),
                       tf.keras.metrics.AUC()])


# Print input size and make fake dataset
print(model.summary())
IShape = model.input_shape
OShape = model.output_shape
TEST = [True,False][1]
if TEST:
    X = [np.random.rand(L,*IShape[0][1:]),np.random.rand(L,*IShape[1][1:])]
    Y = np.random.rand(L,*OShape[1:])
    Y = np.hstack([np.argmax(Y,1).reshape(-1,1),1-np.argmax(Y,1).reshape(-1,1)])
    print(IShape, OShape)
    print(X[0].shape, X[1].shape, Y.shape)
    # Train
    LVAL = int(VAL * L)
    history = model.fit([X[0][:-LVAL],X[1][:-LVAL]],Y[:-LVAL], epochs=EPOCHS, batch_size=BATCH, validation_data=([X[0][-LVAL:],X[1][-LVAL:]],Y[-LVAL:]))
else:


    with open('processed_trace/Dataset0.pkl','rb') as f:
        D = pickle.load(f)
    X1, X20, Y = D['X1'],D['X2'],D['Y']
    ONE_HOT_Y = np.zeros((len(Y),2))
    for i in range(len(Y)):
        ONE_HOT_Y[i,Y[i]] = 1
    ONE_HOT_Y = ONE_HOT_Y.astype('float32')
    L = len(X1)
    LTR = int(L*(1-VAL))
    B = 10
    LTR = LTR//B * B # LTR is approximated to the closest multiple of B :-)
    LVA = L - LTR
    LVA = LVA // B * B # THe same for LVA
    BATCH = BATCH // B * B # And the same for Batch Size

    assert(len(X1)==len(X20)==len(Y))

    X1_TRACKER = []
    for X_ in X1:
        X1_TRACKER.append((ML-len(X_)))

    X2 = [[] for _ in range(len(X20))]
    X2_TRACKER = []
    for i,X_ in enumerate(X20):
        c = 0
        for i_,y_ in enumerate(X_):
            for z in y_:
                X2[i] += [[float(i_),float(z)]]
                c += 1
        X2_TRACKER.append(MI-c) 


    def produce_data(A,B):
        w = list(range(A,B))
        np.random.shuffle(w)
        for i in w:
                yield (
                        ( tf.convert_to_tensor(np.asarray([ (X1[j] + [0.] * X1_TRACKER[j]) for j in range(i-T+1,i+1)]).reshape(1,T,-1,1)), 
                          tf.convert_to_tensor(np.asarray([ (X2[j] + [[0., 0.]] * X2_TRACKER[j]) for j in range(i-T+1,i+1)]).reshape(1,T,-1,2)),
                        ), 
                        tf.convert_to_tensor(ONE_HOT_Y[i:i+1,:].reshape(1,2)),
                      )
        yield None

    # A mini print section for debugging :-) flagged to kill 
    trainD = produce_data(T,LTR)
    #valD = produce_data(LTR+T,L)
    [x1,x2],y = trainD.__next__()
    print(x1.shape, x2.shape, y.shape)
    #	sys.exit(1)



    #OT = ( (tf.TensorSpec(shape=(1, 8, 5712), dtype=tf.float32) , tf.TensorSpec(shape=(8, 5709, 2), dtype=tf.float32)), tf.TensorSpec(shape=(1,2), dtype=tf.float32))
    if False:
        A = tuple([ tuple([  (tf.float32,)              for i in range(5712)  ]) for _ in range(8)])
        B = tuple([ tuple([  (tf.float32,tf.float32)    for i in range(5709)  ]) for _ in range(8)])
        C = tuple(           (tf.float32, tf.float32)                                              )
        OT = tuple([ tuple([A,B]), C])
        print(f'Finished building the output structure')
        trainD = tf.data.Dataset.from_generator(lambda: produce_data(T,LTR), output_types=OT)
        print(f'Finished building the training dataset')
        valD = tf.data.Dataset.from_generator(lambda: produce_data(LTR+T,L), output_types=OT)
        print(f'Finished building the validation dataset')
    else:
        OS = (
                 (tf.TensorSpec(shape=(None,8,5712,1), dtype=tf.float32),
                 tf.TensorSpec(shape=(None,8,5709,2), dtype=tf.float32)),
                 tf.TensorSpec(shape=(None,2), dtype=tf.float32),
            )
        #OS = (
        #        ( (8,5712,1),(8,5709,2) ), (1,2)
        #     )
        print(f'Finished building the output structure')
        trainD = tf.data.Dataset.from_generator(lambda: produce_data(T,LTR), output_signature=OS)#output_types=(tf.float32), output_shapes=OS)
        print(f'Finished building the training dataset')
        valD = tf.data.Dataset.from_generator(lambda: produce_data(LTR+T,L), output_signature=OS)# output_types=(tf.float32), output_shapes=OS)
        print(f'Finished building the validation dataset')
    
    print(f'About to train! :-)')
    history = model.fit(trainD, epochs=1, batch_size=200, validation_data=valD, verbose=2)

    sys.exit(1)
    # Train

# Display results
print(history.history.keys())
f,ax = plt.subplots(1,2,figsize=(15,10))
ax[0].plot(history.history['loss'],label='loss')
ax[0].plot(history.history['val_loss'], label='val loss')
ax[0].legend()
ax[1].plot(history.history['auc'],label='auc')
ax[1].plot(history.history['val_auc'], label='val auc')
ax[1].set_ylim(0,1)
ax[1].legend()																																																																																																																																																																				
plt.show()













