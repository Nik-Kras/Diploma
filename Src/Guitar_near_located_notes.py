import numpy as np
from scipy.signal import hanning
from pydub import AudioSegment
from Src import Api as api

Path = '../Guitar'
file = '/new/Ми мибимоль.wav'

signal = AudioSegment.from_wav(Path + file)
Fs = signal.frame_rate
signal_array = np.array(signal.get_array_of_samples())

harmonics_out = api.harmonics_extraction(signal_array, Fs, plot_Fmax = 70, plot_Fmin = 40)

L = len(signal_array) / 100
L_min = int(45*L)
L_max = int(46*L)
signal_array10 = signal_array[L_min:L_max]

harmonics_out10 = api.harmonics_extraction(signal_array10, Fs, plot_Fmax = 70, plot_Fmin = 40)

zero_support = np.zeros(int(len(signal_array) / 2))
zero_support[1:int(L)] = signal_array[L_min:L_max-2]

harmonics_out10_zero_support = api.harmonics_extraction(zero_support, Fs, plot_Fmax = 70, plot_Fmin = 40)

window_zero_support = np.zeros(int(len(signal_array) / 2))
w = hanning(L_max-L_min-2)
window_zero_support[1:int(L)] = signal_array[L_min:L_max-2] * w

harmonics_out10_zero_support_w = api.harmonics_extraction(window_zero_support, Fs, plot_Fmax = 70, plot_Fmin = 40)