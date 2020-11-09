import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import triang
from scipy.signal import find_peaks             # For harmonics extraction from spectrum
from scipy.interpolate import interp1d          # For making Spectrum smoother
from scipy.interpolate import splev, splrep     # For making Spectrum smoother


def DTFT_harmonics_extraction(sound_array, Fs):
    """
        The functions takes harmonics of signal
        It work based on Furie Transform and scipy
        Algorithms for peak localization

        :param sound_array: signal with harmonics
        :param Fs: sampling frequency
        :return: dictionary with frequencies and its amplitudes
    """
    plt.plot(sound_array)
    plt.show()

    N = len(sound_array)
    sound_array = np.resize(sound_array, (1, N))
    sound_array = np.resize(sound_array, (1*N))

    plt.plot(sound_array)
    plt.show()

    # Useful constants for plots
    N = len(sound_array)
    freq_index = np.linspace(0, round(N / 2), round(N / 2))

    # Find FFT
    Spectrum = 2 * abs(np.fft.fft(sound_array)) / N
    Spectrum = Spectrum[:round(N / 2)]

    # Config harmonics search
    # Minimal freq distance: 5Hz
    # Minimal prominence:    1%
    # Minimal height:        0.09
    min_freq_dist = 60  # Hz
    min_index_dist = round((min_freq_dist / (Fs / 2)) * (N / 2))  # FOR INTERPOLATION   * interp_m    # Index
    min_prominence = 0.25
    min_height = 0.1
    if min_index_dist < 1:
        min_index_dist = 1

    # Find harmonics
    # peaks, _ = find_peaks(Spectrum, distance=min_index_dist, prominence=min_prominence, height=min_height)
    peaks, _ = find_peaks(Spectrum, distance=min_index_dist, prominence=min_prominence, height=min_height)
    f_peaks = Fs * peaks / N  # FOR INTERPOLATION  /interp_m
    a_peaks = Spectrum[peaks]

    # Show result of extraction
    dt = 1 / Fs
    T = N * dt
    t = np.linspace(0, T, N)
    plt.figure(tight_layout='True')
    plt.subplot(2, 1, 1)
    plt.title("Result of Harmonics extraction")
    plt.plot(t, sound_array)
    plt.xlabel("t, s")
    plt.ylabel("Signal")

    freq_interp = Fs * freq_index / N  # Hz
    plt.subplot(2, 1, 2)
    plt.plot(freq_interp, Spectrum)
    plt.plot(f_peaks, Spectrum[peaks], "x")
    plt.xlabel("F, Hz")
    plt.ylabel("Spectrum")
    plt.show()

    harmonics = {}
    for i in range(len(f_peaks)):
        harmonics.update({'Harmonic' + str(i): {'Frequency': [f_peaks[i]], 'Amplitude': [a_peaks[i]]}})
    return harmonics


def test_signal_simpe():
    """
    The function generates an ideal digital signal
    That signal is sum of 3 harmonics of that parameters:
    --- Duration: 5s
    --- Fs: 44kHz
    --- F: 220, 400, 900 Hz
    --- Amp: 1, 2, 0.5 V
    return: signal
    """
    T = 5
    Fs = 44000
    N = T * Fs
    t = np.linspace(0, T, N)
    signal = 1 * np.sin(2 * np.pi * 220 * t) + 2 * np.sin(2 * np.pi * 400 * t) + 0.5 * np.sin(2 * np.pi * 900 * t)
    return signal

def test_signal_changing():
    """
    The function generates an ideal digital signal
    That signal is sum of 3 harmonics
    That changes their amplitudes per time of that parameters:
    --- Duration: 5s
    --- Fs: 44kHz
    --- F: 220, 400, 900 Hz
    --- Amp: 1 (exp(-x)), 2(-kx), 0.5(const) V
    return: signal
    """
    T = 5
    Fs = 44000
    N = T * Fs
    t = np.linspace(0, T, N)
    k = 0.2
    w = 5
    ke = -0.25
    signal = 1 * np.exp(ke*t) * np.sin(2 * np.pi * 220 * t)
    signal += 2 * (abs(np.sin(w*t))*k*t) * np.sin(2 * np.pi * 400 * t)
    signal += 0.5 * np.sin(2 * np.pi * 900 * t)
    return signal

# N = 100
s = triang(51)
plt.plot(s)
plt.show()

