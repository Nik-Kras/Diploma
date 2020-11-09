# General modules
import numpy as np
import unittest
import matplotlib.pyplot as plt

# Testing module
from Src import Api


# Duration: 5s
# Fs:       44kHz
# Harm:
#   220Hz - 1
#   400Hz - 2
#   900Hz - 0.5
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

class HarmonicsExtractionTest(unittest.TestCase):
    """Harmonics Extraction API tests"""

    def test_Control(self):
        """
        Accuracy test of harmonics extraction
        From original math-generated signal
        Accuracy: xxx.xx
        """
        print("id: " + self.id())
        signal = test_signal_simpe()
        Fs = 44000
        Amp = [1, 2, 0.5]
        Freq = [220, 400, 900]
        harmonics = Api.harmonics_extraction(signal, Fs)
        print(harmonics)

        self.assertEqual(len(harmonics), 3)
        for i in range(3):
            self.assertAlmostEqual(harmonics["Harmonic" + str(i)]['Frequency'][0], Freq[i], places=2)
            self.assertAlmostEqual(harmonics["Harmonic" + str(i)]['Amplitude'][0], Amp[i], places=2)

    def test_Shorted_Control_Zero_Support(self):
        """
        Accuracy test of harmonics extraction
        From shorted in "m" times math-generated signal
        That is supported with zeros
        Accuracy: xxx.xx
        """
        print("id: " + self.id())

        # Signal making and constants for shorted signal
        signal = test_signal_simpe()
        Fs = 44000
        N = len(signal)
        m = 40  # Time slices for signal
        k = 10  # len(signal) --> k*len(signal)
        signal = signal[:round(N / m)]
        harmonics = Api.harmonics_extraction_zero_support(signal, Fs, k)
        print(harmonics)

        # Constants for testing
        Amp = [1, 2, 0.5]
        Freq = [220, 400, 900]
        self.assertEqual(len(harmonics), 3)
        for i in range(3):
            self.assertAlmostEqual(harmonics["Harmonic" + str(i)]['Frequency'][0], Freq[i], places=2)
            self.assertAlmostEqual(harmonics["Harmonic" + str(i)]['Amplitude'][0], Amp[i], places=2)

    # execution test


if __name__ == '__main__':
    s = test_signal_changing()
    s = s
    plt.plot(s)
    plt.show()
    harmonics = Api.harmonics_change(s, 44000, window='rect')
    print(harmonics)

    k = 0.2
    ke = -0.25
    w = 5
    f0 = harmonics['Harmonic0']['Frequency']
    t0 = np.array(harmonics['Harmonic0']['Time'])
    A0 = harmonics['Harmonic0']['Amplitude']            # / max(harmonics['Harmonic0']['Amplitude'])
    N0 = len(harmonics['Harmonic0']['Amplitude'])
    f1 = harmonics['Harmonic1']['Frequency']
    t1 = np.array(harmonics['Harmonic1']['Time'])
    A1 = harmonics['Harmonic1']['Amplitude']            # / max(harmonics['Harmonic1']['Amplitude'])
    N1 = len(harmonics['Harmonic1']['Amplitude'])
    f2 = harmonics['Harmonic2']['Frequency']
    t2 = np.array(harmonics['Harmonic2']['Time'])
    A2 = harmonics['Harmonic2']['Amplitude']            # / max(harmonics['Harmonic2']['Amplitude'])
    N2 = len(harmonics['Harmonic2']['Amplitude'])

    print(t0.shape)


    plt.subplot(3, 1, 1)
    plt.ylabel(f0)
    plt.plot(t0, A0)                                # Extraction
    plt.plot(t0, np.exp(ke * t0))                   # Original
    plt.subplot(3, 1, 2)
    plt.ylabel(f1)
    plt.plot(t1, A1)                                # Extraction
    plt.plot(t1, 0.5 * np.ones(t1.shape))           # Original
    plt.ylim(0.4, 0.6)
    plt.subplot(3, 1, 3)
    plt.ylabel(f2)
    plt.plot(t2, A2)                                # Extraction
    plt.plot(t2, 2 * abs(np.sin(w*t2)) * k * t2)    # Original
    plt.show()
    # unittest.main()
