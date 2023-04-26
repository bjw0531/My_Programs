import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt

y, sr = librosa.load('./soundtracks/Beethoven_Virus.wav')

plt.figure(figsize =(16,6))
tempo , _ = librosa.beat.beat_track(y=y)
print(tempo)
librosa.display.waveshow(y=y,sr=sr)
plt.show()
print(len(y))
print(y,sr)