#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import perlin
import tensorflow as tf
import keras as K

from enum import Enum

class SleepQuality(Enum):
    Awake = 0
    REM = 1
    Light = 2
    Deep = 3

class Environment:
    def __init__(self, temperature, brightness, air_quality):
        self.t = temperature
        self.b = brightness
        self.a = air_quality

def generate_data(tmin=15, tmax=22, imin=0, imax=24, d=1440):
    """
    Generates data points with values from [tmin, tmax] and in the
    time interval [imin, imax]

    Returns: A numpy array of dimension (imax - imin)*d x 1
    """

    pnf = perlin.PerlinNoiseFactory(1, 5)
    noise = np.linspace(imin, imax, d, endpoint=False) / imax
    i = 0
    for p in noise:
        noise[i] = pnf(p)
        i = i + 1

    noise = np.abs((noise + 1) * tmax)
    #np.clip(noise, tmin, tmax, out=noise)
    return noise

def adjust_temperature(arg):
    pass

def adjust_environment(env, sq):
    pass

#%%
imin = 0
imax = 24
d = (imax - imin) * 60

temperature = generate_data()
brightness = generate_data(100, 2000, imin, imax, d)
humidty = np.clip(generate_data(0, 100, imin, imax, d), 0, 100)
time = np.linspace(imin, imax, d, endpoint=False)
sleepq = np.clip(np.floor(np.random.normal(2, 2, size=d)), 0, 4)

plt.hist(sleepq, 5, rwidth=0.9)
plt.show()

#%%
plt.figure(figsize=(20,10))
plt.subplot(311)
plt.plot(temperature)
plt.ylabel('temperatures')
plt.subplot(312)
plt.plot(brightness)
plt.ylabel('brightness')
plt.subplot(313)
plt.plot(humidty)
plt.ylabel('humidty')
plt.subplots_adjust(hspace=1)
plt.show()
