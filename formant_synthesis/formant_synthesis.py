"""
Input: phoneme /a/ ->
specify formants (F1=850Hz, F2=1610) ->
generate source signal
    periodic pulse (voiced) <
    noise (unvoicede) 
    ->
apply filters (formants) ->
synthesised speech
"""

import json
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, freqz

# # load formants.json
# with open("formant_synthesis/formants.json", "r") as f:
#     formants = json.load(f)

# print(formants)

fs = 44100

def gen_sourcesig(f=200):
    """
    Generates a sin wave

    Set fundamental frequency to control pitch
    """
    # time in seconds
    t = 1

    samples = np.arange(t * fs) / fs
    signal = np.sin(2 * np.pi * f * samples)
    signal *= 32767
    signal = np.int16(signal)

    return signal

def butter_bandpass(lowcut, highcut, order=5): # https://www.youtube.com/watch?v=OpAvWCIB44U&t=174s
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, order=5):
    b, a = butter_bandpass(lowcut, highcut, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == "__main__":
    sig = gen_sourcesig()
    lowcut = 30.0
    highcut = 300.0

    new = butter_bandpass_filter(sig, lowcut, highcut)

    wavfile.write("source_sig.wav", fs, sig)
    wavfile.write("filtered_sig.wav", fs, new)