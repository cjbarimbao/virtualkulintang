import numpy as np
import sounddevice as sd
import time
import datetime

def sos_interp(a, f, Fs, dt):
    """
        Interpolates the signal values of an input partial from its amplitude and frequency values
        Adapted from sosinterp.m by Franklin Agsaway, 2005
    """

    NperFrame = round(dt * Fs)      # number of samples per frame (original sample length per frame == 44100 * 0.015986 = 705 samples)
    dt = NperFrame / Fs
    Nf = len(a)     # number of frames 

    # Amplitude synthesis interpolation
    a_interp = np.interp(np.arange(0, NperFrame * Nf), np.arange(0, NperFrame * Nf, NperFrame), a)
    # Frequency synthesis interpolation
    f_interp = np.repeat(f, NperFrame)
    # Calculate initial phase points for every frame
    p_points = np.cumsum(2 * np.pi * dt * np.insert(f[:-1], 0, 0)) - 2 * np.pi * np.arange(Nf) * dt * f     # equivalent to startphase - 2 * np.pi * ((i) * dt) * f[i]
    # Phase synthesis interpolation
    p_interp = np.repeat(p_points, NperFrame)

    t = np.arange(0, dt * Nf, 1 / Fs)
    sig = a_interp * np.sin(2 * np.pi * f_interp * t + p_interp)

    return sig

### main code

# Set the sampling frequency
Fs = 44100

# Read first row of the text file containing the synthesis parameters using numpy
data = np.loadtxt('g1_s1_beed_est_l.txt', max_rows=1)

Nf, n = data[:-1].astype(int)
dt = data[-1].astype(float)

# Get the amplitude and frequency values and store in an ndarray
data = np.loadtxt('g1_s1_beed_est_l.txt', skiprows=1)

# Get the amplitude and frequency values and store in an ndarray
an = data[0::2, :].astype(float)
fn = data[1::2, :].astype(float)

# time the execution of the synthesis
start = time.time()

sig = np.sum([sos_interp(an[i], fn[i], Fs, dt) for i in range(1, len(an))], axis=0)



sd.play(sig, Fs)
sd.wait()
# time the execution of the synthesis
end = time.time()
print("Execution time: ", end - start)