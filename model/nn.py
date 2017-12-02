import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import np_utils
from util import *
import tensorflow as tf
import random
tf.logging.set_verbosity(tf.logging.ERROR)

def base_model(classification=False):
    # create model
    model = Sequential()

    model.add(Dense(2000, input_dim=29, activation='relu'))
    model.add(Dense(500, activation='relu'))
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(150, activation='relu'))
    # model.add(Dense(50, activation='tanh'))
    # model.add(Dense(10, activation='relu'))

    # output layer
    if classification:
        model.add(Dense(1, activation='linear'))
    else:
        model.add(Dense(4, activation='linear'))

    # Compile model
    return model
 
def train_model():
    X, y, X2, y2 = get_feature_sets_regression()
    epochs = 50
    best_acc = 0

    model = base_model()
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    for epoch in xrange(epochs):
        print 'Doing epoch {}...'.format(epoch+1)
        model.fit(np.array(X), np.array(y), epochs=1, batch_size=32)
        print 'Evaluating model...'
        score = model.evaluate(X, y)[1]
        print score
        print("Training Accuracy: %.2f%%" % (score*100))
        score = model.evaluate(X2, y2)[1]
        print("Test Accuracy: %.2f%%" % (score*100))

        if score > best_acc and score > .8:
            model.save('ff{}_{}small.h5'.format(epoch+1, score))
            best_acc = score

        print


if __name__ == '__main__':
    train_model()

