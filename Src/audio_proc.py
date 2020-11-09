import numpy as np
import os
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt

# Список видимых файлов/директорий
d = '.'
print(os.listdir(d))

# Загрузить без ffmpeg можно только аудио .wav
# Другие форматы запустить не удалось
audio = AudioSegment.from_wav('Guitar\\Sound2.wav')
Fs = audio.frame_rate
data = np.asarray(audio.get_array_of_samples())
N = data.size

# print info
print("\n\nINFO BLOCK\n")
print("Time of audio = " + str(len(audio)) + "ms")
print("Samples of audio = " + str(len(audio.raw_data)))
print("Samples of data = " + str(N) )
print("data type = ", type(data))

# Plot audio line
t = np.linspace(0, len(audio), N)
fig = plt.figure()   # Создание объекта Figure
plt.plot(t, data)
plt.show()

# Find FFT
Fmax = 1500                     # Задаю пределы графика спектра
Nmax = round( N * Fmax / Fs  )  # Индекс соотв. предела спектра
S_data = np.fft.fft(data)
Short_S_data = abs(S_data[:Nmax]) / max(abs(S_data[:Nmax]))
freq = np.fft.fftfreq(t.shape[-1]) * Fs

# print info
print("Freq size = ", freq.size)
print("Index for Fmax = ", Nmax)
print("Fmax = ", Fmax)
print("Fs = ", Fs)

# Plot FFT
plt.plot(freq[:Nmax], Short_S_data )
plt.show()


# Find Base frequency
LowNote = 50 # Hz
minDist = Nmax * LowNote/(4 * Fmax)
print(minDist)
peaks, _ = find_peaks(Short_S_data, distance=minDist, prominence=(0.01, 1))
f = Fmax * peaks / Nmax
f = f.astype(dtype = np.int32)
F0 = f[0]               # Основная частота

plt.plot(freq[:Nmax], Short_S_data )
plt.plot(f, Short_S_data[peaks], "x")
plt.show()

print(f)
print("F base = ", F0)

# Find Picks
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
