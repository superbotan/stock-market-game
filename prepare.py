import finam_data as fd

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


#fc = fd.LoadFile("US1.MU_170101_180101.test.txt")
fc = fd.LoadFile("SPBEX.AMD_170101_180101.txt")

fc = fd.RecalcSplines(fc)

#fc = fd.CalcSignalV1(fc, intervals_ct, morning_step, commision_calc)
fc = fd.CalcSignalV2(fc, commision_calc)

fc = fd.SignalResultCalc(fc, commision_display)

fd.WriteToFileCalcresults(fc, "res.test.txt")

fd.WriteToFileStudy(fc, "study.test.txt")