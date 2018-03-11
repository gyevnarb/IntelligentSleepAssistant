#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import perlin
import tensorflow as tf
import json
import time
import datetime

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Input, LSTM, Reshape, Lambda, RepeatVector
from keras.layers import Embedding

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

def preprocess_data(sleep_json, mbed_json):
    X = parse_sleep(sleep_json)
    Y = parse_mbed(mbed_json)
    return (x, Y)

def parse_mbed(raw_text):
    out = json.loads(raw_text)

    first = 0.0

    Y = np.empty(shape=(1,))

    for d in out:
        Y = np.append(Y, d["airData"])
        Y = np.append(Y, d["lightData"])
        Y = np.append(Y, d["moistureData"])
        Y = np.append(Y, d["tempData"])
        date = d["date"]
        hours = d["time"]
        t = date + " " + hours
        unix_time = time.mktime(datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S").timetuple())
        if (first is 0.0):
            first = unix_time
        Y = np.append(Y, unix_time - first)

    return Y

def parse_sleep(raw_text):
    out = json.loads(raw_text)
    sleep = out['sleep'][0]

    duration = sleep['duration']
    X = np.asarray(duration) / 1000 #Convert to seconds

    efficiency = sleep['efficiency']

    isMainSleep = sleep['isMainSleep']
    if (isMainSleep):
        X = np.append(X, 1)
    else:
        X = np.append(X, 0)

    levels = sleep['levels']

    summary = levels['summary']
    s_deep = summary['deep']
    X = np.append(X, s_deep['count'])
    X = np.append(X, s_deep['minutes'])
    X = np.append(X, s_deep['thirtyDayAvgMinutes'])

    s_light = summary['light']
    X = np.append(X, s_light['count'])
    X = np.append(X, s_light['minutes'])
    X = np.append(X, s_light['thirtyDayAvgMinutes'])

    s_rem = summary['rem']
    X = np.append(X, s_rem['count'])
    X = np.append(X, s_rem['minutes'])
    X = np.append(X, s_rem['thirtyDayAvgMinutes'])

    s_wake = summary['wake']
    X = np.append(X, s_wake['count'])
    X = np.append(X, s_wake['minutes'])
    X = np.append(X, s_wake['thirtyDayAvgMinutes'])

    data = levels['data']
    for d in data:
        X = np.append(X, level_to_num(d['level']))
        X = np.append(X, d['seconds'])

    return X

def level_to_num(level_str):
    if (level_str == 'wake'):
        return 0
    elif (level_str == 'rem'):
        return 1
    elif (level_str == 'light'):
        return 2
    elif (level_str == 'deep'):
        return 3
    else:
        return -1

def env_model(Tx, n_a, n_vals):
    pass
    #X = Input()

def generate_random_data():
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

f = open("sample.json")
X = parse_sleep(f.read())
print(X)
f = open('sample2.json')
Y = parse_mbed(f.read())
print(Y)
f.close()
