from time import strftime, gmtime
import datetime
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
import numpy as np
from keras.models import model_from_json
import os.path

class FinamData:
    def __init__(self, line):
        elements = line.replace('\n', '').split('\t')
        self.date = int(elements[2])
        self.time = int(elements[3])
        self.open = float(elements[4])
        self.high = float(elements[5])
        self.low = float(elements[6])
        self.close = float(elements[7])
        self.vol = int(elements[8])

        self.m_time = int(elements[9])
        self.start_val = float(elements[10])

        self.signal = float(elements[11])

        self.vol_max = float(elements[12])
        self.vol_avg = float(elements[13])

        self.spline6 = float(elements[14])
        self.spline12 = float(elements[15])
        self.spline36 = float(elements[16])
        self.spline50 = float(elements[17])
        self.spline105 = float(elements[18])
        self.spline210 = float(elements[19])
        self.spline420 = float(elements[20])
        self.spline1050 = float(elements[21])


        self.close_1 = float(elements[22])
        self.close_2 = float(elements[23])
        self.close_3 = float(elements[24])
        self.close_4 = float(elements[25])
        self.close_5 = float(elements[26])
        self.close_6 = float(elements[27])
        self.close_7 = float(elements[28])
        self.close_8 = float(elements[29])

        self.vol_1 = float(elements[30])
        self.vol_2 = float(elements[31])
        self.vol_3 = float(elements[32])
        self.vol_4 = float(elements[33])
        self.vol_5 = float(elements[34])
        self.vol_6 = float(elements[35])
        self.vol_7 = float(elements[36])
        self.vol_8 = float(elements[37])

        self.d_close = float(elements[38])

        self.d_spline6 = float(elements[39])
        self.d_spline12 = float(elements[40])
        self.d_spline36 = float(elements[41])
        self.d_spline50 = float(elements[42])
        self.d_spline105 = float(elements[43])
        self.d_spline210 = float(elements[44])
        self.d_spline420 = float(elements[45])
        self.d_spline1050 = float(elements[46])

    def lp(self, pers = 0.05, d_pers = 0.001):
        r = [

            #float((self.time - 40000 - self.m_time)) / 80000,
            #(self.close - self.start_val) / self.start_val / pers,

            #(self.spline6 - self.start_val) / self.start_val / pers,
            #(self.spline12 - self.start_val) / self.start_val / pers,
            #(self.spline36 - self.start_val) / self.start_val / pers,
            #(self.spline50 - self.start_val) / self.start_val / pers,
            #(self.spline105 - self.start_val) / self.start_val / pers,
            #(self.spline210 - self.start_val) / self.start_val / pers,
            #(self.spline420 - self.start_val) / self.start_val / pers,
            #(self.spline1050 - self.start_val) / self.start_val / pers,

            #(self.close_1 - self.start_val) / self.start_val / pers,
            #(self.close_2 - self.start_val) / self.start_val / pers,
            #(self.close_3 - self.start_val) / self.start_val / pers,
            #(self.close_4 - self.start_val) / self.start_val / pers,
            #(self.close_5 - self.start_val) / self.start_val / pers,
            #(self.close_6 - self.start_val) / self.start_val / pers,
            #(self.close_7 - self.start_val) / self.start_val / pers,
            #(self.close_8 - self.start_val) / self.start_val / pers,

            #(self.vol - self.vol_avg) / self.vol_avg,

            #(self.vol_1 - self.vol_avg) / self.vol_avg,
            #(self.vol_2 - self.vol_avg) / self.vol_avg,
            #(self.vol_3 - self.vol_avg) / self.vol_avg,
            #(self.vol_4 - self.vol_avg) / self.vol_avg,
            #(self.vol_5 - self.vol_avg) / self.vol_avg,
            #(self.vol_6 - self.vol_avg) / self.vol_avg,
            #(self.vol_7 - self.vol_avg) / self.vol_avg,
            #(self.vol_8 - self.vol_avg) / self.vol_avg

            float((self.time - 40000 - self.m_time)) / 80000,
            self.d_close / self.close / d_pers,

            self.d_spline6 / self.spline6 / d_pers,
            self.d_spline12 / self.spline12 / d_pers * 2,
            self.d_spline36 / self.spline36 / d_pers * 6,
            self.d_spline50 / self.spline50 / d_pers * 10,
            self.d_spline105 / self.spline105 / d_pers * 20,
            self.d_spline210 / self.spline210 / d_pers * 40,
            self.d_spline420 / self.spline420 / d_pers * 80,
            self.d_spline1050 / self.spline1050 / d_pers * 200,

            (self.close_1 - self.close) / self.close / pers,
            (self.close_2 - self.close) / self.close / pers,
            (self.close_3 - self.close) / self.close / pers,
            (self.close_4 - self.close) / self.close / pers,
            (self.close_5 - self.close) / self.close / pers,
            (self.close_6 - self.close) / self.close / pers,
            (self.close_7 - self.close) / self.close / pers,
            (self.close_8 - self.close) / self.close / pers,

            (self.vol - self.vol_avg) / self.vol_avg,
            #(-self.signal),

            (self.vol_1 - self.vol_avg) / self.vol_avg,
            (self.vol_2 - self.vol_avg) / self.vol_avg,
            (self.vol_3 - self.vol_avg) / self.vol_avg,
            (self.vol_4 - self.vol_avg) / self.vol_avg,
            (self.vol_5 - self.vol_avg) / self.vol_avg,
            (self.vol_6 - self.vol_avg) / self.vol_avg,
            (self.vol_7 - self.vol_avg) / self.vol_avg,
            (self.vol_8 - self.vol_avg) / self.vol_avg,

            (self.close - self.spline6) / self.close / pers,
            (self.close - self.spline12) / self.close / pers,
            (self.close - self.spline36) / self.close / pers,
            (self.close - self.spline50) / self.close / pers,
            (self.close - self.spline105) / self.close / pers,
            (self.close - self.spline210) / self.close / pers,
            (self.close - self.spline420) / self.close / pers,
            (self.close - self.spline1050) / self.close / pers,
        ]

        #print(r)

        return r

    def ap(self):
        return [
            self.signal*0.8
        ]


def LoadFile(path):
    f = open(path, 'r')
    fc = []
    i = 0
    for line in f.readlines():
        if i > 0:

            l = FinamData(line)

            fc.append(l)

        i = i + 1

    f.close()
    return fc


def WriteModel(model, prefix = '', ext = 'test.txt'):
    t = gmtime()

    m_fn = prefix+'model_'+strftime("%Y-%m-%d_%H_%M_%S", t)+'.test.txt'
    w_fn = prefix+'model_w_' + strftime("%Y-%m-%d_%H_%M_%S", t) + '.test.txt'

    json_string = model.to_json()
    #w = model.get_weights()

    model_out = open(prefix+'model.' + ext, 'w')
    model_out_t = open(m_fn, 'w')
    #model_w_out = open(prefix+'model_w.txt', 'w')
    #model_w_out_t = open(w_fn, 'w')


    model_out.write(json_string)
    model_out_t.write(json_string)

    model.save_weights(prefix+'model_w.' + ext)
    model.save_weights(w_fn)

    #model_w_out.write(w)
    #model_w_out_t.write(w)

    model_out.close()
    model_out_t.close()
    #model_w_out.close()
    #model_w_out_t.close()
    #model = model_from_json(json_string)


def CanLoadModel(prefix = '', ext = 'test.txt'):
    return os.path.isfile(prefix+ 'model.' + ext) and os.path.isfile(prefix+'model_w.' + ext)

def LoadModel(prefix = '', ext = 'test.txt'):
    f_m = open(prefix+ 'model.' + ext, 'r')
    #f_w = open(prefix+'model_w.txt', 'r')

    m_s = f_m.read()
    #w_s = f_w.read()

    model = model_from_json(m_s)

    #model.set_weights(w_s)
    model.load_weights(prefix+'model_w.' + ext, by_name=False)

    f_m.close()
    #f_w.close()

    return model
