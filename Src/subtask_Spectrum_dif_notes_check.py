import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from Src import Api as api
"""
Нужно проверить одинаковые ли спектры одного инструмента для разных нот. Сохраняется ли тембр

"""


Path = '../Guitar'
file = '/new/60 нот.wav'

signal = AudioSegment.from_wav(Path + file)
Fs = signal.frame_rate
signal_array = np.array(signal.get_array_of_samples())

harmonics_out = api.harmonics_extraction(signal_array, Fs, plot_Fmax = 1500, plot_Fmin = 40)

t0 = 2
t1 = 3
t2 = 4.1
t3 = 5.1
t4 = 6.1
t5 = 7
t6 = 8
t7 = 8.9
t8 = 9.8

t = list(map(int,np.array([t0, t1, t2, t3, t4, t5, t6, t7, t8])*2*Fs)) # IDK why *2

s1 = signal_array[t[0]:t[1]]
s2 = signal_array[t[1]:t[2]]
s3 = signal_array[t[2]:t[3]]
s4 = signal_array[t[3]:t[4]]
s5 = signal_array[t[4]:t[5]]
s6 = signal_array[t[5]:t[6]]
s7 = signal_array[t[6]:t[7]]
s8 = signal_array[t[7]:t[8]]

# 175k - 250k


harmonics_out1 = api.harmonics_extraction(s1, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out2 = api.harmonics_extraction(s2, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out3 = api.harmonics_extraction(s3, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out4 = api.harmonics_extraction(s4, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out5 = api.harmonics_extraction(s5, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out6 = api.harmonics_extraction(s6, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out7 = api.harmonics_extraction(s7, Fs, plot_Fmax=1250, plot_Fmin=0)
harmonics_out8 = api.harmonics_extraction(s8, Fs, plot_Fmax=1250, plot_Fmin=0)