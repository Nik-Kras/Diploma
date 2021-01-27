import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import triang, hamming, hanning
from scipy.signal import find_peaks             # For harmonics extraction from spectrum
from scipy.interpolate import interp1d          # For making Spectrum smoother
from scipy.interpolate import splev, splrep     # For making Spectrum smoother

# This function returns dictionary with
# Frequencies and amplitudes of harmonics
# (works good for rect and bad for all other)
def harmonics_extraction(sound_array, Fs, plots='yes', plot_Fmax = 1500, plot_Fmin = 0):
    """
    The functions takes harmonics of signal
    It work based on Furie Transform and scipy
    Algorithms for peak localization

    :param sound_array: signal with harmonics
    :param Fs: sampling frequency
    :return: dictionary with frequencies and its amplitudes
    """

    # Useful constants for plots
    N = len(sound_array)
    freq_index = np.linspace(0, round(N / 2), round(N / 2))

    '''
    # Show sound
    dt = 1/Fs
    T = N*dt
    t = np.linspace(0, T, N)
    fig = plt.figure()
    plt.plot(t, sound_array)
    plt.show()
    '''

    # Find FFT
    # Because of formatting m4a --> wav spectrum may be copied
    # So, optionally S may be divided twice

    Spectrum = 2 * abs(np.fft.fft(sound_array)) / N
    Spectrum = Spectrum[:round(N / 2)]

    # Optionally
    Spectrum = Spectrum[:round(N / 4)]
    freq_index = np.linspace(0, round(N / 4), round(N / 4))
    Spectrum = Spectrum
    '''
    plt.plot(Spectrum)
    plt.show()
    '''

    # Config harmonics search
    # Minimal freq distance: 5Hz
    # Minimal prominence:    1%
    # Minimal height:        0.09
    min_freq_dist = 10                                                                           # Hz
    min_index_dist = round((min_freq_dist / (Fs/2)) * (N/2)) # FOR INTERPOLATION   * interp_m    # Index
    min_prominence = 0.55       # 0.25
    min_height = 5    # , height=min_height (0.2)
    if min_index_dist < 1:
        min_index_dist = 1

    # Find harmonics
    peaks, _ = find_peaks(Spectrum, distance=min_index_dist, prominence=min_prominence, height=min_height)
    f_peaks = Fs * peaks / N
    a_peaks = Spectrum[peaks]


    if plots=='yes':
        # Show result of extraction
        dt = 1 / Fs
        T = N * dt
        T = T/2                     # IDK why, but time is twice bigger than it should be, so I divide it
        t = np.linspace(0, T, N)
        plt.figure(tight_layout='True')
        plt.subplot(2, 1, 1)
        plt.title("Result of Harmonics extraction")
        plt.plot(t, sound_array)
        plt.xlabel("t, s")
        plt.ylabel("Signal")

        freq_interp = Fs * freq_index / N  # Hz
        plt.subplot(2, 1, 2)
        plt.plot(freq_interp[:len(Spectrum)], Spectrum)
        plt.plot(f_peaks, Spectrum[peaks], "x")
        plt.xlabel("F, Hz")
        plt.ylabel("Spectrum")
        plt.xlim((plot_Fmin, plot_Fmax))
        plt.show()

    harmonics = {}
    for i in range(len(f_peaks)):
        harmonics.update({'Harmonic'+str(i):{'Frequency': [f_peaks[i]], 'Amplitude': [a_peaks[i]]}})
    return harmonics

def harmonics_extraction_zero_support(sound_array, Fs, k, window):
    """
    The functions takes harmonics of signal
    It work based on Furie Transform and scipy
    Algorithms for peak localization
    Also (k-1)*len(signal) zeros are added
    To the signal, so it works well for short signals

    :param sound_array: signal with harmonics
    :param Fs: sampling frequency
    :param k: expansion factor
    :param window: defines window-function for Fourier Analysis
            -- 'rect'       B-spilne window 1st order
            -- 'triangle'   B-spline window 2nd order
            -- 'hamming'
            -- 'hann'
    :return: dictionary with frequencies and its amplitudes
    """
    N = len(sound_array)
    w = 1
    if window == "triangle":
        w = triang(N)
    elif window == "hamming":
        w = hamming(N)
    elif window =='hann':
        w = hanning(N)
    elif window != "rect":
        print("Not correct window name!\nWill use rect!")

    sound_array = sound_array * w

    # If "rect" - use just it
    sound_array_support = np.zeros(round(k * len(sound_array)))
    sound_array_support[0:len(sound_array)] = k * sound_array[:]

    harmonics = harmonics_extraction(sound_array_support, Fs, plots='no')
    return harmonics

def harmonics_change(sound_array, Fs, window):
    """
    The function calculates time changes of harmonics per time.
    That changes defines a tone of the signal/sound

    :param sound_array: signal with harmonics
    :param Fs: sampling frequency
    :param window: defines window-function for Fourier Analysis
            -- 'rect'
            -- 'triangle'
            -- 'hamming'
    :return: time dependencies of each harmonic
    """

    # Add zero support to be divided by @length_short_signal@ !!!
    short_L = 1500  # int(len(sound_array)/220)

    thousand = short_L - len(sound_array) % short_L
    zero_support = [0] * thousand

    list_sound_array = list(sound_array)
    list_sound_array += zero_support
    sound_array = np.array(list_sound_array)

    ##########################################################################################

    count_short_signal = int(np.ceil(len(sound_array) / short_L))
    signals_matrix = np.reshape(sound_array, (count_short_signal, short_L))

    T = 5
    k = 60
    harmonics_per_time = harmonics_extraction_zero_support(signals_matrix[0], Fs, k, window)
    for i in range(len(harmonics_per_time)):
        harmonics_per_time['Harmonic' + str(i)]['Time'] = [0]

    # Find amplitude for each short signal
    for i in range(1, count_short_signal):
        harmonics = harmonics_extraction_zero_support(signals_matrix[i], Fs, k, window)

        # Parse both dictionaries.
        # Append to previous harmonics
        # And add new if needed
        for j in range(len(harmonics)):
            new_harmonic = 'True'
            for z in range(len(harmonics_per_time)):
                delta = 25
                val_delta = harmonics_per_time['Harmonic' + str(z)]['Frequency'][0] - \
                            harmonics['Harmonic' + str(j)]['Frequency'][0]

                # If harmonic is finded - append new amplitude value
                if abs(val_delta) < delta:
                    harmonics_per_time['Harmonic' + str(z)]['Amplitude'].append(harmonics['Harmonic'+str(j)]['Amplitude'][0])
                    harmonics_per_time['Harmonic' + str(z)]['Time'].append(i*T/count_short_signal)
                    new_harmonic = 'False'

                # print(harmonics_per_time)
                # print("************************************")

            # Add new harmonics if needed
            # harmonics[j] is not in harmonics_per_time[:]
            # .Different harmonics number form both dictionaries
            # .Could have the same frequency, so check 'Frequency', not number
            if new_harmonic == 'True':
                harmonics_per_time.update(
                    {'Harmonic' + str(len(harmonics_per_time)): harmonics['Harmonic' + str(j)]})  # Here is problem
                harmonics_per_time['Harmonic' + str(len(harmonics_per_time)-1)]['Time'] = [0]


    return harmonics_per_time
