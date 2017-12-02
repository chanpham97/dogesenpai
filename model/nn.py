import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import np_utils
from keras.models import load_model
from keras.optimizers import SGD
from sklearn.utils import shuffle
from util import *
import tensorflow as tf
import random
tf.logging.set_verbosity(tf.logging.ERROR)

def base_model(classification=False):
    # create model
    model = Sequential()

    model.add(Dense(300, input_dim=29, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(2000, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(290, activation='relu'))

    # output layer
    if classification:
        model.add(Dense(4, activation='softmax'))
    else:
        model.add(Dense(4, activation='linear'))

    # Compile model
    return model
 
def train_model(classification=False):
    if classification:
        X, y, X2, y2 = get_feature_sets_classification()
        loss = 'categorical_crossentropy'
        # {'Platinum': 0.1, 'Bronze': 0.2, 'Silver': 0.4, 'Gold': 0.3}
    else:
        X, y, X2, y2 = get_feature_sets_regression()
        loss = 'mean_squared_error'
    epochs = 50
    best_acc = 0
    print loss
    model = base_model(classification=classification)
    # optimizer = SGD(lr=0.00001)
    model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])
    for epoch in xrange(epochs):
        X, y = shuffle(X, y)
        print 'Doing epoch {}...'.format(epoch+1)
        model.fit(np.array(X), np.array(y), epochs=1, batch_size=32)
        print 'Evaluating model...'
        # score = model.evaluate(X, y)[1]
        # print score
        # print("Training Accuracy: %.2f%%" % (score*100))
        score = model.evaluate(X2, y2)[1]
        print model.predict(np.array([X[0]])), y[0]
        print("Test Accuracy: %.2f%%" % (score*100))

        if score > best_acc and score >= .75:
            model.save('cls{}_{}.h5'.format(epoch+1, score))
            best_acc = score

        print


if __name__ == '__main__':
    train_model(classification=True)

