from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

import numpy as np


import finam_study as fs


dir_n = 'models_arch/v2_'

pers = 0.05

fc = fs.LoadFile("study.test.txt")



for i in range (0, 100):
    print(i)
    if not fs.CanLoadModel(dir_n):
        print('new_model')
        model = Sequential()
        model.add(Dense(30, input_dim=36))
        model.add(Activation('tanh'))
        model.add(Dense(20))
        model.add(Activation('tanh'))
        model.add(Dense(3))
        model.add(Activation('tanh'))
        model.add(Dense(1))
        model.add(Activation('tanh'))
    else:
        print('load_model')
        model = fs.LoadModel(dir_n)

    sgd = SGD(lr=0.01)

    model.compile(loss='mean_squared_error', optimizer=sgd)

    for i in range(5, len(fc)-1):
        ld_s = []
        ad_s = []

        ld_s.append(fc[i].lp(pers))
        ad_s.append(fc[i].ap(v=1))

        X = np.array(ld_s)
        y = np.array(ad_s)

        if (i%1000 == 0):
            print(i, '')
            print(' of ', '')
            print(len(fc))

            model.fit(X, y, batch_size=1, epochs=1, verbose = 1)
        else:
            model.fit(X, y, batch_size=1, epochs=1, verbose=0)


    fs.WriteModel(model, dir_n)