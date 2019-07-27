#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

data1, samplerate1 = sf.read(sys.argv[1])
data2, samplerate2 = sf.read(sys.argv[2])

assert samplerate1 == samplerate2
print(data1.shape)

# corr = np.correlate(data1[:,1], data2[:,1], "full")
fftlen = pow(2,24);
corr = np.fft.irfft(np.fft.rfft(data1[:fftlen,1]) * np.conj(np.fft.rfft(data2[:fftlen,1])))
minpos = np.argmax(corr)
print(minpos)
print(minpos / samplerate1)
plt.plot(corr)
plt.show()
sf.write("1.wav", data1[minpos:], samplerate1)
sf.write("2.wav", data2, samplerate1)
