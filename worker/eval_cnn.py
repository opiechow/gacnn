'''Train a simple deep CNN on the CIFAR10 small images dataset.
It gets to 75% validation accuracy in 25 epochs, and 79% after 50 epochs.
(it's still underfitting at that point, though).
'''

import helper_classes

def eval_network(individual, epochs, seed):
    assert(isinstance(individual, helper_classes.Individual))

    import pickle
    import numpy.random
    numpy.random.seed(seed)
    import keras
    from keras.datasets import cifar10
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Activation, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    import os

    batch_size = 32
    num_classes = 10
    num_predictions = 20
    save_dir = os.path.join(os.getcwd(), 'saved_models')
    model_name = 'keras_cifar10_trained_model.h5'

    # The data, split between train and test sets:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # Convert class vectors to binary class matrices.
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    layers = individual.genotype
    model = Sequential()
    for idx, layer in enumerate(layers):
        if idx == 0:
            model.add(Conv2D(layer, (3, 3), padding='same',
                             input_shape=x_train.shape[1:]))
            model.add(Activation('relu'))
        else:
            model.add(Conv2D(layer, (3, 3)))
            model.add(Activation('relu'))
            ## add 1 pooling layer in the middle
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

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              shuffle=False)

    # Save model and weights
    #if not os.path.isdir(save_dir):
    #   os.makedirs(save_dir)
    #model_path = os.path.join(save_dir, model_name)
    #model.save(model_path)

    # Score trained model.
    scores = model.evaluate(x_test, y_test, verbose=1)
    print("layers : " + str(layers))
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])
    individual.loss = scores[0]
    individual.score = scores[1]
    with open("result",'wb') as f:
        pickle.dump(individual, f)
