#!/usr/bin/env python3
import json
import sys
import subprocess
import numpy as np
from mkl_fft._numpy_fft import rfft, irfft
# from numpy.fft import rfft, irfft
# from scipy.fftpack import rfft, irfft
import soundfile as sf
import mkl
# print(mkl.set_num_threads(4))
print(mkl.get_max_threads())

START = 0

def fftconv(data1, data2):
    return irfft(rfft(data1) * data2)

def open_with_ffmpeg(filename, rate):
    ffmpeg = subprocess.Popen(
        ['ffmpeg', '-v', 'quiet', '-ss', str(START),
         '-i', filename, '-ac', '1', '-ar', str(rate), '-f', 'wav', 'pipe:1'],
        stdout=subprocess.PIPE)
    return ffmpeg.stdout

def find(needleFilename, haystackFilename, rate):
    fftlen = 2**25
    shift = fftlen >> 1
    # try:
    #     needle, rate2 = sf.read(needleFilename, frames=fftlen, start=START*rate)
    # except RuntimeError:
    needle, rate2 = sf.read(open_with_ffmpeg(needleFilename,rate).fileno(), frames=shift)
    # print(np.linalg.norm(needle) / needle.shape[0])
    needle /= np.linalg.norm(needle)
    print(needle.shape[0])
    needle = np.array(needle)
    needle.resize(fftlen)
    assert rate2 == rate

    pos = 0
    res = []
    needleFFT = np.conj(rfft(needle))
    for haystack in sf.blocks(haystackFilename, blocksize=fftlen, fill_value=0, overlap=shift, always_2d=True):
        # if len(haystack) < fftlen:
        #     haystack = np.resize(haystack, fftlen)
        # haystack /= np.linalg.norm(haystack)
        corr = abs(fftconv(haystack[:,0], needleFFT))
        corr = corr[:shift]
        corr /= np.linalg.norm(haystack[:,0])
        minpos = np.argmax(corr)
        mincorr = corr[minpos]
        if mincorr > 0.01:
            print("{} at {} + {}/{}".format(mincorr, pos, minpos, fftlen))
        # if minpos > fftlen/2:
        #     minpos -= fftlen
        minpos += pos
        # print('{} ({:.3f}s): {}'.format(minpos, minpos/rate, mincorr))
        pos += shift
        res.append((minpos, mincorr))
        if mincorr > 0.2:
            break
    return res

def ffprobe(filename):
    sub = subprocess.run(
            ['ffprobe', '-print_format', 'json', '-v', 'quiet', '-show_streams',
             filename], stdout=subprocess.PIPE, check=True)
    return json.loads(sub.stdout)

def main():
    duration = ffprobe(sys.argv[1])['streams'][0]['duration']
    print(duration)
    info = sf.info(sys.argv[2])
    correlations = find(sys.argv[1], sys.argv[2], info.samplerate)
    correlations.sort(key=lambda x: x[1], reverse=True)
    print(correlations[:5])
    print(list(map(lambda x: x[0]/48000, correlations[:5])))
    if correlations[0][1] < 0.05:
        return
    if len(sys.argv) < 4:
        return
    print('Writing output file')
    copy, rate = sf.read(sys.argv[2], frames=int(float(duration)*info.samplerate),
                         start=correlations[0][0]-START)
    sf.write(sys.argv[3], copy, rate)
    # subprocess.run(
    #     ['sox', sys.argv[2], 'output.flac',
    #      'trim', str((correlations[0][0]-START)/48000), '+' + duration], check=True)
        # ['ffmpeg', '-v', 'quiet', '-ss', str((correlations[0][0]-START)/48000), '-y',
        #  '-t', duration, '-i', sys.argv[2], 'output.flac'], check=True)

if __name__ == "__main__":
    main()
