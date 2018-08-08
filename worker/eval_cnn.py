'''Train a simple deep CNN on the CIFAR10 small images dataset.
It gets to 75% validation accuracy in 25 epochs, and 79% after 50 epochs.
(it's still underfitting at that point, though).
'''
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.datasets import cifar10
from keras import backend as K
import tensorflow as tf
from common import helper_classes
import random as rn
import numpy as np
import pickle
import keras
import os


def set_random_seed(seed):
    os.environ['PYTHONHASHSEED'] = '0'
    np.random.seed(seed)
    rn.seed(seed)
    session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
    tf.set_random_seed(seed)
    sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
    K.set_session(sess)


def eval_network(individual, epochs, seed):
    assert(isinstance(individual, helper_classes.Individual))
    set_random_seed(seed)
    batch_size = 32
    num_classes = 10

    print("Layers : " + str(individual.phenotype))
    # The data, split between train and test sets:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # Convert class vectors to binary class matrices.
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    layers = individual.phenotype
    model = Sequential()
    for idx, layer in enumerate(layers):
        if idx == 0:
            model.add(Conv2D(layer, (3, 3), padding='same',
                             input_shape=x_train.shape[1:]))
            model.add(Activation('relu'))
        else:
            model.add(Conv2D(layer, (3, 3)))
            model.add(Activation('relu'))
            # add 1 pooling layer in the middle
            if (idx + 1) == (len(layers) // 2):
                model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        validation_data=(x_test, y_test),
                        shuffle=False)

    # Score trained model.
    scores = model.evaluate(x_test, y_test, verbose=1)

    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])
    individual.loss = scores[0]
    individual.score = scores[1]
    individual.training_history = str(history.history)
    with open("result",'wb') as f:
        pickle.dump(individual, f)
