import numpy as np
from scipy.signal import hanning
from pydub import AudioSegment
from Src import Api as api

Path = '../Guitar'
file = '/new/Where is my mind - для анализа - соло.wav'

signal = AudioSegment.from_wav(Path + file)
Fs = signal.frame_rate
signal_array = np.array(signal.get_array_of_samples())

harmonics_out = api.harmonics_extraction(signal_array, Fs, plot_Fmax = 700, plot_Fmin = 40)

# df = 5 Hz is okay for analysis 0.2s * Fs = 8820
slice_size = 88200
number = slice_size - len(signal_array) % slice_size
zero_support = [0] * number                             # Zeros to be added for
list_sound_array = list(signal_array)                   # Signal array division on "slice size"
list_sound_array += zero_support
sound_array = np.array(list_sound_array)

m = int(len(sound_array) / slice_size)                  # Count of batches
m2 = int(2*m - 1)                                       # With regarding to shift
shifted_signal_slices = np.zeros((m2 ,slice_size))
h_ss = int(slice_size/2)                                # Half Slice Size

w = hanning(slice_size)

for i in range(1, m-1):
    shifted_signal_slices[2 * i - 1] = sound_array[(i-1)*slice_size : i*slice_size] * w
    shifted_signal_slices[2 * i] = sound_array[(i-1)*slice_size + h_ss : i*slice_size + h_ss] * w

t = h_ss/Fs
harmonics_changes = []
for i in range(1, len(shifted_signal_slices)):

    harmonics_out = api.harmonics_extraction(shifted_signal_slices[i], Fs, plot_Fmax=500, plot_Fmin=40)

    t += h_ss/Fs
    print("Time: " + str(t) + "s")
    print(harmonics_out)
    harmonics_changes.append(harmonics_out)
