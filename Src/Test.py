from Src.audio_processing import audio_to_peaks

Path = 'Guitar\\Sound2.wav'
Fmax = 1500

f_peak, a_peak = audio_to_peaks(Path, Fmax)

print("Peaks: ")
print(f_peak)
