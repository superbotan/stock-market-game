import math

class FinamData:
    def __init__(self, line):
        elements = line.replace('\n', '').split(',')

        self.date = int(elements[2])
        self.time = int(elements[3])
        self.open = float(elements[4])
        self.high = float(elements[5])
        self.low = float(elements[6])
        self.close = float(elements[7])
        self.vol = int(elements[8])

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

def RecalcSplines(fc):
    cur_start_time = 0
    cur_date = 0
    start_val = 0

    vol_max = 0
    vol_avg = 0
    vol_n = 0

    for i in range(0, len(fc)):
        if (cur_date < fc[i].date and fc[i].time > 30000):
            cur_start_time = fc[i].time
            cur_date = fc[i].date
            start_val = fc[i].close

        if (fc[i].vol > vol_max):
            vol_max = fc[i].vol

        vol_avg = vol_avg + fc[i].vol
        vol_n = vol_n + 1

        fc[i].morning_start = cur_start_time
        fc[i].spline6 = float(0)
        fc[i].spline12 = float(0)
        fc[i].spline36 = float(0)
        fc[i].spline50 = float(0)
        fc[i].spline105 = float(0)
        fc[i].spline210 = float(0)
        fc[i].spline420 = float(0)
        fc[i].spline1050 = float(0)
        fc[i].start_val = start_val
        fc[i].ext_up = 0
        fc[i].ext_down = 0
        fc[i].signal = 0

        if i > 1050:
            for j in range(0, 6):
                fc[i].spline6 = fc[i].spline6 + fc[i - j].close
            for j in range(0, 12):
                fc[i].spline12 = fc[i].spline12 + fc[i - j].close
            for j in range(0, 36):
                fc[i].spline36 = fc[i].spline36 + fc[i - j].close
            for j in range(0, 50):
                fc[i].spline50 = fc[i].spline50 + fc[i - j].close
            for j in range(0, 105):
                fc[i].spline105 = fc[i].spline105 + fc[i - j].close
            for j in range(0, 210):
                fc[i].spline210 = fc[i].spline210 + fc[i - j].close
            for j in range(0, 420):
                fc[i].spline420 = fc[i].spline420 + fc[i - j].close
            for j in range(0, 1050):
                fc[i].spline1050 = fc[i].spline1050 + fc[i - j].close

            fc[i].spline6 = fc[i].spline6 / 6
            fc[i].spline12 = fc[i].spline12 / 12
            fc[i].spline36 = fc[i].spline36 / 36
            fc[i].spline50 = fc[i].spline50 / 50
            fc[i].spline105 = fc[i].spline105 / 105
            fc[i].spline210 = fc[i].spline210 / 210
            fc[i].spline420 = fc[i].spline420 / 420
            fc[i].spline1050 = fc[i].spline1050 / 1050

    for i in range(0, len(fc)):
        fc[i].vol_max = vol_max
        fc[i].vol_avg = vol_avg / vol_n

    return fc

def CalcSignalV1(fc, intervals_ct, morning_step, commision_calc):
    for i in range(0, len(fc)):
        fc[i].signal_ext = 0
        signal = 0
        if (fc[i].time == (fc[i].morning_start + morning_step)):
            current_min_ext = fc[i].close
            current_max_ext = fc[i].close
            current_time = fc[i].time
            ku = i
            kd = i
            k = i
            for j in range(i + 1, i + intervals_ct):
                if (current_min_ext > fc[j].close):
                    current_min_ext = fc[j].close
                    kd = j
                if (current_max_ext < fc[j].close):
                    current_max_ext = fc[j].close
                    ku = j
                if ((fc[j].close - current_min_ext) / fc[j].close) > commision_calc:
                    signal = 1
                    k = kd
                    break
                if ((current_max_ext - fc[j].close) / fc[j].close) > commision_calc:
                    signal = -1
                    k = ku
                    break

            if signal != 0:
                exts = []
                exts.append(k)
                for r in range(k + 1, i + intervals_ct - 1):
                    if (fc[r].close > fc[r - 1].close and fc[r].close >= fc[r + 1].close
                            or fc[r].close < fc[r - 1].close and fc[r].close <= fc[r + 1].close):
                        exts.append(r)
                exts.append(i + intervals_ct)

                m = 0
                while m >= 0 and m < (len(exts) - 1):
                    # Если сигнал совпадает с направленем между экстремумами
                    if (signal > 0 and fc[exts[m]].close <= fc[exts[m + 1]].close):
                        for r in range(exts[m], exts[m + 1]):
                            fc[r].signal = signal
                        m = m + 1
                        continue
                    if (signal < 0 and fc[exts[m]].close >= fc[exts[m + 1]].close):
                        for r in range(exts[m], exts[m + 1]):
                            fc[r].signal = signal
                        m = m + 1
                        continue

                    # Если сигнал > 0 то ищем следующий сигналвниз до дельты
                    # Если такой сигнал есть и он следуюий, то -1
                    # Если такой сигнал есть и он не следующий, то ищем максимальный сигнал между ними и до него идём
                    # Если нет такого сигнала ищем макс сигнал от этого до последнего и в нём выходим
                    if (signal > 0):
                        m_st = len(exts)
                        found = 0
                        for mi in range(m + 1, len(exts)):
                            if ((fc[exts[m]].close - fc[exts[mi]].close) / fc[exts[m]].close) > commision_calc:
                                m_st = mi
                                found = 1
                                break

                        f_max = fc[exts[m]].close
                        m_max = m
                        for mi in range(m + 1, m_st):
                            if f_max > fc[exts[mi]].close:
                                f_max = fc[exts[mi]].close
                                m_max = mi

                        if m_max == m and found == 0:
                            m = -1
                            break

                        if m_max == m and found == 1:
                            signal = -1
                            continue

                        if m_max != m:
                            for r in range(exts[m], exts[m + 1]):
                                fc[r].signal = signal
                            m = m + 1
                            continue

                    if (signal < 0):
                        m_st = len(exts)
                        found = 0
                        for mi in range(m + 1, len(exts)):
                            if ((fc[exts[mi]].close - fc[exts[m]].close) / fc[exts[m]].close) > commision_calc:
                                m_st = mi
                                found = 1
                                break

                        f_max = fc[exts[m]].close
                        m_max = m
                        for mi in range(m + 1, m_st):
                            if f_max < fc[exts[mi]].close:
                                f_max = fc[exts[mi]].close
                                m_max = mi

                        if m_max == m and found == 0:
                            m = -1
                            break

                        if m_max == m and found == 1:
                            signal = 1
                            continue

                        if m_max != m:
                            for r in range(exts[m], exts[m + 1]):
                                fc[r].signal = signal
                            m = m + 1
                            continue
    return fc

def SignalResultCalc(fc, commision_display, delta = 0.2):
    v = 0
    v_ext = 0
    for i in range(0, len(fc)):
        fc[i].tax_value = 0
        fc[i].op_value = 0
        fc[i].tax_value_ext = 0
        fc[i].op_value_ext = 0
        if (fc[i].signal > delta and fc[i - 1].signal <= delta):
            if (v > 0):
                ch = v - fc[i].close
                fc[i].op_value = ch
            fc[i].tax_value = v * commision_display
            v = fc[i].close
        if (fc[i].signal < -delta and fc[i - 1].signal >= -delta):
            if (v > 0):
                ch = fc[i].close - v
                fc[i].op_value = ch
            fc[i].tax_value = v * commision_display
            v = fc[i].close
        if (delta > fc[i].signal and fc[i].signal > -delta
                and (fc[i - 1].signal <= - delta or fc[i - 1].signal >= delta)
                and v > 0):
            ch = fc[i - 1].signal * (fc[i].close - v)
            fc[i].op_value = ch
            fc[i].tax_value = v * commision_display
            v = 0

        if (fc[i].signal_ext > delta and fc[i - 1].signal_ext <= delta):
            if (v_ext > 0):
                ch = v_ext - fc[i].close
                fc[i].op_value_ext = ch
            fc[i].tax_value_ext = v_ext * commision_display
            v_ext = fc[i].close
        if (fc[i].signal_ext < -delta and fc[i - 1].signal_ext >= -delta):
            if (v_ext > 0):
                ch = fc[i].close - v_ext
                fc[i].op_value_ext = ch
            fc[i].tax_value_ext = v_ext * commision_display
            v_ext = fc[i].close
        if (delta > fc[i].signal_ext and fc[i].signal_ext > -delta
                and (fc[i - 1].signal_ext  <= - delta or fc[i - 1].signal_ext  >= delta)
                and v_ext > 0):
            ch = fc[i - 1].signal_ext * (fc[i].close - v_ext)
            fc[i].op_value_ext = ch
            fc[i].tax_value_ext = v_ext * commision_display
            v_ext = 0

    return fc

def WriteToFileCalcresults(fc, path):
    f_out = open(path, 'w')

    f_out.write('\t')
    f_out.write('\t')
    f_out.write('date\t')
    f_out.write('time\t')
    f_out.write('open\t')
    f_out.write('high\t')
    f_out.write('low\t')
    f_out.write('close\t')
    f_out.write('vol\t')

    f_out.write('signal\t')
    f_out.write('signal_ext\t')

    f_out.write('signal_d\t')
    f_out.write('signal_ext_d\t')

    f_out.write('op_value\t')
    f_out.write('tax_value\t')

    f_out.write('op_value_ext\t')
    f_out.write('tax_value_ext\t')

    f_out.write('\n')

    v = 0

    for i in range(0, len(fc)):
        f_out.write('\t')
        f_out.write('\t')
        f_out.write(str(fc[i].date) + '\t')
        f_out.write(str(fc[i].time) + '\t')
        f_out.write(str(fc[i].open) + '\t')
        f_out.write(str(fc[i].high) + '\t')
        f_out.write(str(fc[i].low) + '\t')
        f_out.write(str(fc[i].close) + '\t')
        f_out.write(str(fc[i].vol) + '\t')

        f_out.write(str(fc[i].signal) + '\t')
        f_out.write(str(fc[i].signal_ext) + '\t')

        f_out.write(str(fc[i].signal * fc[i].spline1050 * 0.01 + fc[i].spline1050 * 1) + '\t')
        f_out.write(str(fc[i].signal_ext * fc[i].spline1050 * 0.01 + fc[i].spline1050 * 1) + '\t')

        f_out.write(str(fc[i].op_value) + '\t')
        f_out.write(str(fc[i].tax_value) + '\t')

        f_out.write(str(fc[i].op_value_ext) + '\t')
        f_out.write(str(fc[i].tax_value_ext) + '\t')

        f_out.write('\n')

    f_out.close()


def WriteToFileStudy(fc, path, morning_step, evening_step, min_step):
    f_out = open(path, 'w')

    f_out.write('\t')
    f_out.write('\t')
    f_out.write('date\t')
    f_out.write('time\t')
    f_out.write('open\t')
    f_out.write('high\t')
    f_out.write('low\t')
    f_out.write('close\t')
    f_out.write('vol\t')

    f_out.write('m_time\t')
    f_out.write('start_val\t')

    f_out.write('signal\t')

    f_out.write('vol_max\t')
    f_out.write('vol_avg\t')

    f_out.write('spline6\t')
    f_out.write('spline12\t')
    f_out.write('spline36\t')
    f_out.write('spline50\t')
    f_out.write('spline105\t')
    f_out.write('spline210\t')
    f_out.write('spline420\t')
    f_out.write('spline1050\t')

    f_out.write('close_1\t')
    f_out.write('close_2\t')
    f_out.write('close_3\t')
    f_out.write('close_4\t')
    f_out.write('close_5\t')
    f_out.write('close_6\t')
    f_out.write('close_7\t')
    f_out.write('close_8\t')

    f_out.write('vol_1\t')
    f_out.write('vol_2\t')
    f_out.write('vol_3\t')
    f_out.write('vol_4\t')
    f_out.write('vol_5\t')
    f_out.write('vol_6\t')
    f_out.write('vol_7\t')
    f_out.write('vol_8\t')

    f_out.write('d_close\t')

    f_out.write('d_spline6\t')
    f_out.write('d_spline12\t')
    f_out.write('d_spline36\t')
    f_out.write('d_spline50\t')
    f_out.write('d_spline105\t')
    f_out.write('d_spline210\t')
    f_out.write('d_spline420\t')
    f_out.write('d_spline1050\t')

    f_out.write('\n')

    v = 0

    for i in range(0, len(fc)):
        if i > 8 and fc[i - 1].spline1050 > 0 \
                and fc[i].time >= fc[i].morning_start + morning_step \
                and fc[i].time <= fc[i].morning_start + morning_step + evening_step - min_step:
            f_out.write('\t')
            f_out.write('\t')
            f_out.write(str(fc[i].date) + '\t')
            f_out.write(str(fc[i].time) + '\t')
            f_out.write(str(fc[i].open) + '\t')
            f_out.write(str(fc[i].high) + '\t')
            f_out.write(str(fc[i].low) + '\t')
            f_out.write(str(fc[i].close) + '\t')
            f_out.write(str(fc[i].vol) + '\t')

            f_out.write(str(fc[i].morning_start) + '\t')
            f_out.write(str(fc[i].start_val) + '\t')

            f_out.write(str(fc[i].signal) + '\t')

            f_out.write(str(fc[i].vol_max) + '\t')
            f_out.write(str(fc[i].vol_avg) + '\t')

            f_out.write(str(fc[i].spline6) + '\t')
            f_out.write(str(fc[i].spline12) + '\t')
            f_out.write(str(fc[i].spline36) + '\t')
            f_out.write(str(fc[i].spline50) + '\t')
            f_out.write(str(fc[i].spline105) + '\t')
            f_out.write(str(fc[i].spline210) + '\t')
            f_out.write(str(fc[i].spline420) + '\t')
            f_out.write(str(fc[i].spline1050) + '\t')

            f_out.write(str(fc[i - 1].close) + '\t')
            f_out.write(str(fc[i - 2].close) + '\t')
            f_out.write(str(fc[i - 3].close) + '\t')
            f_out.write(str(fc[i - 4].close) + '\t')
            f_out.write(str(fc[i - 5].close) + '\t')
            f_out.write(str(fc[i - 6].close) + '\t')
            f_out.write(str(fc[i - 7].close) + '\t')
            f_out.write(str(fc[i - 8].close) + '\t')

            f_out.write(str(fc[i - 1].vol) + '\t')
            f_out.write(str(fc[i - 2].vol) + '\t')
            f_out.write(str(fc[i - 3].vol) + '\t')
            f_out.write(str(fc[i - 4].vol) + '\t')
            f_out.write(str(fc[i - 5].vol) + '\t')
            f_out.write(str(fc[i - 6].vol) + '\t')
            f_out.write(str(fc[i - 7].vol) + '\t')
            f_out.write(str(fc[i - 8].vol) + '\t')

            f_out.write(str(fc[i].close - fc[i - 1].close) + '\t')

            f_out.write(str(fc[i].spline6 - fc[i - 1].spline6) + '\t')
            f_out.write(str(fc[i].spline12 - fc[i - 1].spline12) + '\t')
            f_out.write(str(fc[i].spline36 - fc[i - 1].spline36) + '\t')
            f_out.write(str(fc[i].spline50 - fc[i - 1].spline50) + '\t')
            f_out.write(str(fc[i].spline105 - fc[i - 1].spline105) + '\t')
            f_out.write(str(fc[i].spline210 - fc[i - 1].spline210) + '\t')
            f_out.write(str(fc[i].spline420 - fc[i - 1].spline420) + '\t')
            f_out.write(str(fc[i].spline1050 - fc[i - 1].spline1050) + '\t')

            f_out.write('\n')

    f_out.close()
