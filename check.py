from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

import numpy as np

import finam_data as fd


import finam_study as fs


# Prepare

# ticks count
tic = 1
# calc interval
intervals_ct = int(5*60 / tic)

# interval size in file
min_step = 100 * tic

# start calc after morning
morning_step = 10000 - min_step

# commission for calculate
commision_calc = float(0.003)

# commission for display
commision_display = float(0.001)

# learn period
evening_step = 5*10000

fc = fd.LoadFile("SPBEX.AMD_180101_180701.txt")

fc = fd.RecalcSplines(fc)

#fc = fd.CalcSignalV1(fc, intervals_ct, morning_step, commision_calc)
fc = fd.CalcSignalV2(fc, commision_calc)




fd.WriteToFileStudy(fc, "check.test.txt")


# Check

dir_n = 'models_arch/'

pers = 0.05

fc = fs.LoadFile("check.test.txt")

#fc = fd.CalcSignalV1(fc, intervals_ct, morning_step, commision_calc)

model = fs.LoadModel(dir_n)

for i in range(0, len(fc)):
    ld_s = []
    ld_s.append(fc[i].lp(pers))
    X = np.array(ld_s)
    y = model.predict(X)
    fc[i].signal_ext = y[0][0]
    #if i> 0 and fc[i].date != fc[i - 1].date:
    #    fc[i-1].signal = 0
    #    fc[i-1].signal_ext = 0



fc = fd.SignalResultCalc(fc, commision_display)

fd.WriteToFileCalcresults(fc, "res.check.test.txt")
