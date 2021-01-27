from pydub import AudioSegment
from Src import Api as api

Path = '../Guitar'
file = '/new/Гитара в разных местах.wav'

signal = AudioSegment.from_wav(Path + file)
Fs = signal.frame_rate
signal_array = signal.get_array_of_samples()

harmonics_out = api.harmonics_extraction(signal_array, Fs)

######################## IDK why, but time in is twice long... ####################
t0 = 5
t1 = 18
s1 = signal_array[t0*Fs:t1*Fs]
harmonics_out1 = api.harmonics_extraction(s1, Fs)

t2 = 31
s2 = signal_array[t1*Fs:t2*Fs]
harmonics_out2 = api.harmonics_extraction(s2, Fs)

t3 = 41
s3 = signal_array[t2*Fs:t3*Fs]
harmonics_out3 = api.harmonics_extraction(s3, Fs)

t4 = 51
s4 = signal_array[t3*Fs:t4*Fs]
harmonics_out4 = api.harmonics_extraction(s4, Fs)

t5 = 60
s5 = signal_array[t4*Fs:t5*Fs]
harmonics_out5 = api.harmonics_extraction(s5, Fs)

t6 = 74
s6 = signal_array[t5*Fs:t6*Fs]
harmonics_out6 = api.harmonics_extraction(s6, Fs)

t7 = 79
s7 = signal_array[t6*Fs:t7*Fs]
harmonics_out7 = api.harmonics_extraction(s7, Fs)

t8 = 89
s8 = signal_array[t7*Fs:t8*Fs]
harmonics_out8 = api.harmonics_extraction(s8, Fs)

t9 = 104
s9 = signal_array[t8*Fs:t9*Fs]
harmonics_out9 = api.harmonics_extraction(s9, Fs)