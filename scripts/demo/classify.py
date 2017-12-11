import keras
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from keras import optimizers
from keras.layers.advanced_activations import ELU, PReLU, LeakyReLU
from keras.layers import Dense, Dropout, Activation, Flatten

import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.models import Model


from sklearn import svm
model = Sequential()
model.add(Conv2D(8, (3, 3), padding='same',
                 input_shape=(513, 800, 3)))
model.add(Activation('relu'))
model.add(Conv2D(8, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(16, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(16, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.25))

model.add(Flatten())
#model.add(Dense(10))
model.add(Activation('relu'))
#model.add(Dropout(0.5))
model.add(Dense(57))
model.add(Activation('softmax'))

model.summary()

# initiate RMSprop optimizer
opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

model2 = Model(inputs=model.input, outputs=model.get_layer('flatten_1').output)

import subprocess
import matplotlib.pyplot
import os
import matplotlib.pyplot as plt


def train():
	rootdir = './train/'

	spectograms = []
	spect_read = []
	spectograms_ids = []
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file.endswith('png'): 
				try:
					x = plt.imread(subdir+'/'+file)
				except:
					continue
				if str(x.shape) == '(513, 800, 3)': 
					spect_read.append(x)
                	#print(subdir) 
					name = subdir.replace(rootdir, '')
                	#print(name)
                	#name = name.replace('/spects', "")
					spectograms_ids.append(name)
					spectograms.append(file)
	x_train = spect_read
	y_train = spectograms_ids


	svm_x_train = []
	svm_y_train = []
	for i in range(len(x_train)):
		x_1 = np.expand_dims(x_train[i], axis=0)
		flatten_2_features = model2.predict(x_1)
		svm_x_train.append(flatten_2_features)
		svm_y_train.append(dummy_y[i])

	svm_x_train = np.array(svm_x_train)
	clf = svm.SVC(kernel='rbf', class_weight='balanced')
	dataset_size = len(svm_x_train)
	svm_x_train = np.array(svm_x_train).reshape(dataset_size,-1)
	svm_y_train = np.array(svm_y_train)
	svm_y_train = [np.where(r==1)[0][0] for r in svm_y_train]

	clf.fit(svm_x_train, svm_y_train)
	print('model trained')


def test(): 
	rootdir = './test/'
	spectograms = []
	spect_read = []
	spectograms_ids = []
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file.endswith('png'): 
				try:
					x = plt.imread(subdir+'/'+file)
				except:
					continue
				if str(x.shape) == '(513, 800, 3)': 
					spect_read.append(x)
					name = subdir.replace(rootdir, '')
                	#name = name.replace('/spects', "")
					spectograms.append(file)
	x_test = spect_read


	encoder = LabelEncoder()
	y_temp_train = y_train
	encoder.fit(y_temp_train)
	encoded_Y = encoder.transform(y_temp_train)
	dummy_y = np_utils.to_categorical(encoded_Y)

	svm_x_test = []
	for i in range(len(x_test)):
		x_1 = np.expand_dims(x_test[i], axis=0)
    	#x_1 = preprocess_input(x_1)
		flatten_2_features = model2.predict(x_1)
		svm_x_test.append(flatten_2_features)
	svm_x_test = np.array(svm_x_test)	


	dataset_size = len(svm_x_test)
	svm_x_test = np.array(svm_x_test).reshape(dataset_size,-1)
	print(clf.predict(svm_x_test))
