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
from scipy import signal
import matplotlib.pyplot as plt

# load formants.json
with open("formant_synthesis/formants.json", "r") as f:
    formants = json.load(f)

# samples per second
fs = 16000

def gen_sourcesig(f, t=np.linspace(0, 1, fs)):
    """
    Generates a sawtooth wave at set frequency and timespan
    """
    return signal.sawtooth(2 * np.pi * f * t)

def butter_bandpass(sig, order, low, high):
    sos = signal.butter(order, [low, high], btype="bandpass", fs=fs, output="sos")
    return signal.sosfilt(sos, sig)

def synth_vowel(x, vowel):
    outputs = []

    # filter for each vowel formant
    # bandwidth determines how wide the formant is
    for freq, bandwidth in formants[vowel]:
        # get Q
        Q = freq / bandwidth

        # get numerator coefficients and denominator coefficients
        # create resonant bandpass filter centred at freq and bandwidths
        b, a = signal.iirpeak(freq, Q, fs=fs)
        
        # apply filter
        y = signal.lfilter(b, a, x)
        outputs.append(y)

    # combine individual formants
    return np.sum(outputs, axis=0)

def save_signal(sig, fp):
    data = np.int16(sig * 32767)
    wavfile.write(fp, fs, data)

if __name__ == "__main__":
    t = np.linspace(0, 1, fs)
    sig = gen_sourcesig(200, t)
    # filtered_sig = butter_bandpass(sig, 4, 300, 3000)
    filtered_sig = synth_vowel(sig, "o")

    save_signal(sig, "source_sig.wav")
    save_signal(filtered_sig, "filtered_sig.wav")

    fig, axs = plt.subplots(2)
    fig.suptitle("Source signal and filtered signal")
    axs[0].plot(t, sig)
    axs[1].plot(t, filtered_sig)
    plt.show()