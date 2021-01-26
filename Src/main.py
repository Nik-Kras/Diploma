from pydub import AudioSegment
from Src import Api as api

Path = '../Guitar/'
file = 'Sound2_edit.wav'

if __name__ == '__main__':

    signal = AudioSegment.from_wav('../Guitar/Sound2_edit.wav')
    Fs = signal.frame_rate

    api.harmonics_change(signal, Fs, 'hann')
