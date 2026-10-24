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

# load formants.json
with open("formant_synthesis/formants.json", "r") as f:
    formants = json.load(f)

print(formants)

def gen_sourcesig(f=200):
    """
    Generates a sin wave

    Set fundamental frequency to control pitch
    """

    fs = 44100
    # time in seconds
    t = 1

    samples = np.arange(t * fs) / fs
    signal = np.sin(2 * np.pi * f * samples)
    signal *= 32767
    signal = np.int16(signal)
    wavfile.write("source_sig.wav", fs, signal)

def apply_filters():
    pass

if __name__ == "__main__":
    gen_sourcesig()