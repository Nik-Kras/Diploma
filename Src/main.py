import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import json

from Src import Api as api

Path = 'Guitar/'
file = 'Sound2_edit.wav'

if __name__ == '__main__':

    '''
    # Load signal - get harmonics from spectrum
    signal = AudioSegment.from_wav(Path + file)
    Fs = signal.frame_rate
    signal_array = signal.get_array_of_samples()

    harmonics_out = api.harmonics_extraction(signal_array, Fs)

    freq = []
    amp = []
    for harm in harmonics_out:
        print(harm)
    print(freq)
    '''
################################################################ DOES NOT WORK CORRECTLY #########################
    signal = AudioSegment.from_wav(Path + file)
    Fs = signal.frame_rate
    signal_array = signal.get_array_of_samples()

    harmonics_out = api.harmonics_change(signal_array, Fs, 'hann')

    print(harmonics_out)

    # Delete all freq > 1500
    for i in range(1, len(harmonics_out)):
        if harmonics_out['Harmonic' + str(i)]['Frequency'][0] > 1500:
            del harmonics_out['Harmonic' + str(i)]

    print(json.dumps(harmonics_out, indent=4))

    # Show count of samples for each frequency
    for i in harmonics_out.keys():
        print("Frequency: " + str(harmonics_out[i]['Frequency'][0]))
        print("Samples: " + str(len(harmonics_out[i]['Amplitude'])))
        print("************************")

    # Find dividers of harmonics counter
    M = len(harmonics_out.keys())
    divider = M-1
    while divider>2:
        if M%divider == 0:
            break
        divider -= 1

    sec_divider = int(M/divider)

    # Plot all harmonics
    index_cnt = 0
    for i in range(1,divider):
        for j in range(1, sec_divider+1):
            index = list(harmonics_out.keys())[index_cnt]

            f0 = harmonics_out[index]['Frequency'][0]
            t0 = harmonics_out[index]['Time']
            A0 = harmonics_out[index]['Amplitude']

            plt.subplot(sec_divider, 1, j)
            plt.ylabel(f0)
            plt.plot(t0, A0)

            index_cnt += 1

        plt.show()

    '''
    print(json.dumps(harmonics_out, indent=4))
    print(harmonics_out.keys())

    f0 = harmonics_out['Harmonic0']['Frequency']
    t0 = np.array(harmonics_out['Harmonic0']['Time'])
    A0 = harmonics_out['Harmonic0']['Amplitude'] / max(harmonics_out['Harmonic0']['Amplitude'])
    N0 = len(harmonics_out['Harmonic0']['Amplitude'])
    f1 = harmonics_out['Harmonic1']['Frequency']
    t1 = np.array(harmonics_out['Harmonic1']['Time'])
    A1 = harmonics_out['Harmonic1']['Amplitude'] / max(harmonics_out['Harmonic1']['Amplitude'])
    N1 = len(harmonics_out['Harmonic1']['Amplitude'])
    f2 = harmonics_out['Harmonic2']['Frequency']
    t2 = np.array(harmonics_out['Harmonic2']['Time'])
    A2 = harmonics_out['Harmonic2']['Amplitude'] / max(harmonics_out['Harmonic2']['Amplitude'])
    N2 = len(harmonics_out['Harmonic2']['Amplitude'])

    print(t0.shape)

    plt.subplot(3, 1, 1)
    plt.ylabel(f0)
    plt.plot(t0, A0)  # Extraction
    plt.subplot(3, 1, 2)
    plt.ylabel(f1)
    plt.plot(t1, A1)  # Extraction
    #plt.ylim(0.4, 0.6)
    plt.subplot(3, 1, 3)
    plt.ylabel(f2)
    plt.plot(t2, A2)  # Extraction
    plt.show()
    '''