
from matplotlib import pyplot
from keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical

from numpy import mean
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import fashion_mnist

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD

import keras
from keras.utils.vis_utils import plot_model


def load_dataset():

	(trainX, trainY), (testX, testY) = fashion_mnist.load_data()

	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))

	trainY = to_categorical(trainY)
	testY = to_categorical(testY)
	return trainX, trainY, testX, testY

def pix(train, test):

	train_norm = train.astype('float32')
	test_norm = test.astype('float32')

	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0

	return train_norm, test_norm

# define cnn model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(10, activation='softmax'))

	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

def evaluate_model(dataX, dataY, n_folds=5):
	scores, histories = list(), list()

	kfold = KFold(n_folds, shuffle=True, random_state=1)

	for train_ix, test_ix in kfold.split(dataX):

		model = define_model()
		keras.utils.plot_model(model, "FashionModel.png", show_shapes=True)

		trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
		# fit model
		history = model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(testX, testY), verbose=0)

		_, acc = model.evaluate(testX, testY, verbose=0)
		print('> %.3f' % (acc * 100.0))

		scores.append(acc)

	return scores




def run():

	trainX, trainY, testX, testY = load_dataset()

	trainX, testX = pix(trainX, testX)

	scores = evaluate_model(trainX, trainY)
	print("model evaluated")

	print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores) * 100, std(scores) * 100, len(scores)))


run()