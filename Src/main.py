import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    n = 10   # Primary digits count
    N = 100  # Secondary digits count
    dur = 1 # Duration 5s
    f = 1   # Freq 1Hz
    tn = np.linspace(0, 0.9, n)
    triangle = np.append(tn[0:5]*np.ones(int(n/2)), np.zeros(int(n/2))) - np.append(np.zeros(int(n/2)), -1+tn[5:]*np.ones(int(n/2)))

    sn = np.sin(2*np.pi*f*tn)
    sN = np.append(triangle*sn, np.zeros(N))

    spec_n = np.fft.fftshift(2 * abs(np.fft.fft(sn, n=200)) / n)
    # spec_n = spec_n[:round(n / 2)]
    spec_N = np.fft.fftshift((N/n) * 2 * abs(np.fft.fft(sN)) / len(sN) )
    # spec_N = spec_N[:round(N / 2)]

    # freqn = [x for x in np.linspace(-n/2, n/2, len(spec_n))]
    # freqN = [x for x in np.linspace(-n/2, n/2, len(spec_N))]

    plt.subplot(4, 1, 1)
    plt.stem(tn, sn)
    plt.subplot(4, 1, 2)
    plt.stem( spec_n)
    plt.subplot(4, 1, 3)
    plt.stem(sN)
    plt.subplot(4, 1, 4)
    plt.stem( spec_N)
    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""
    plt.subplot(2, 1, 1)
    plt.plot(signal_sinc)
    plt.subplot(2, 1, 2)
    plt.subplot(signal_conv[:])
    plt.show()
"""