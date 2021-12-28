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
    L = len(X1)
    assert(len(X1)==len(X20)==len(Y))
    X1 = np.asarray([X_ + [0] * (ML-len(X_)) for X_ in X1]).reshape(len(X1),-1,1)
    X2 = np.asarray([([(i_,y_) for i_,y_ in enumerate(X_)] + [(0,0)] * (MI-len(X_)) ) for X_ in X20])
    LTR = int(L*(1-VAL))
    B = 10
    LTR = LTR//B * B # LTR is approximated to the closest multiple of B :-)
    LVA = L - LTR
    LVA = LVA // B * B # THe same for LVA
    BATCH = BATCH // B * B # And the same for Batch Size
    print(f'X1\'s shape is: {X1.shape}, X2\'s shape is: {X2.shape}, Ltrain and Lval are {LTR},{LVA}. The batch size has been readjusted to {BATCH}')
    def produce_data(A,B):
        w = list(range(A,B))
        np.random.shuffle(w)
        for i in w:
            yield [X1[i-T+1:i+1,:,:],X2[i-T+1,:i+1,:]]
        yield None

    trainD = produce_data(T,LTR)
    valD = produce_data(LTR+T,L)

    print(Y)
    sys.exit(1)
    # Train
    history = model.fit([X[0][:-LVAL],X[1][:-LVAL]],Y[:-LVAL], epochs=EPOCHS, batch_size=BATCH, validation_data=([X[0][-LVAL:],X[1][-LVAL:]],Y[-LVAL:]))

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













