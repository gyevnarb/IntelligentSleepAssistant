%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import perlin
import tensorflow as tf
import json
import time
import datetime
import requests as r
import io
from keras.models import Sequential
from keras.layers import Dense, LSTM

n_y = 4
n_x = 3
n_a = 32
batch_size = 2

def parse_mbed(mbed_json, n_y=n_y):
    first = 0.0

    Y = []

    for mbed in mbed_json:
        data = mbed['data']
        for d in data:
            Y_ = []
            Y_.append(d["airData"])
            Y_.append(d["lightData"])
            Y_.append(d["moistureData"])
            Y_.append(d["tempData"])
            # date = d["date"]
            # hours = d["time"]
            # t = date + "T" + hours
            # unix_time = to_unix_time(t)
            # if (first is 0.0):
            #     first = unix_time
            # Y = np.append(Y, unix_time - first)
            Y.append(Y_)

    return Y

def parse_sleep(in_json, n_x=n_x):
    X = []
    m = 0
    for sleep in in_json:
        m = m + 1
        duration = sleep['duration']
        X_head = np.asarray(duration) / 1000 # Convert to seconds

        efficiency = sleep['efficiency']
        X_head = np.append(X_head, efficiency)

        levels = sleep['levels']

        X_data = []
        passed = 0.0
        data = levels['data']
        for d in data:
            X_ = []
            X_.append(level_to_num(d['level']))
            secs = d['seconds']
            X_.append(secs)
            passed = passed + secs
            X_.append(passed)
            X_data.append(X_)
        X.append(X_data)

    return (X_head, X, m)

def level_to_num(level_str):
    if (level_str == 'awake'):
        return 0
    elif (level_str == 'restless'):
        return 1
    elif (level_str == 'asleep'):
        return 2
    else:
        return -1

def to_unix_time(date_time):
    return time.mktime(datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S").timetuple())

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

def generate_random_data(m, plot=True):
    imin = 16
    imax = 24
    d = (imax - imin) * 60

    Y = []

    for i in range(m):
        temperature = generate_data()
        brightness = generate_data(100, 2000, imin, imax, d)
        humidity = generate_data(0, 100, imin, imax, d)
        humidity = humidity / np.max(humidity) * 100
        co2 = generate_data(0, 1, imin, imax, d)
        zipped = zip(temperature, brightness, humidity, co2)

        rjt = []
        for (t, b, h, c) in zipped:
            tmp = [t, b, h, c]
            rjt.append(tmp)
        #    rjt.append({'airData': c, 'lightData': b, 'moistureData': h, 'tempData': t})

        Y.append(rjt)

    if (plot):
        plt.figure(figsize=(20,10))
        plt.subplot(411)
        plt.plot(temperature)
        plt.ylabel('temperatures')
        plt.subplot(412)
        plt.plot(brightness)
        plt.ylabel('brightness')
        plt.subplot(413)
        plt.plot(humidity)
        plt.ylabel('humidty')
        plt.subplot(414)
        plt.plot(co2)
        plt.ylabel('CO2')
        plt.subplots_adjust(hspace=1)
        plt.show()

    return Y

def fetch_data():
    base_url = "http://34.245.151.229:5000/"
    sleep_url = "sleep"
    mbed_url = "data"
    resp = r.get(base_url + sleep_url)
    sleep_json = resp.json()
    #resp = r.get(base_url + mbed_url)
    f = open('../../data.json', 'r')
    mbed_json = json.loads(f.read())#resp.json()
    return (sleep_json, mbed_json)

def create_vectors(sleep_json, mbed_json):
    (X_head, X, m) = parse_sleep(sleep_json)
    #Y = parse_mbed(mbed_json)

    #Creating pre-generated data and aligning dimension
    X_ = []
    lengths = []
    for l in X:
        lengths.append(len(l))
    max_len = np.max(lengths)
    for l in X:
        if (len(l) < 20):
            continue
        else:
            tmp = l
            for j in range(max_len - len(l)):
                tmp.append([0, 0, 0])
        X_.append(tmp)
    X = np.asarray(X_)
    m = X.shape[0]
    Y_ = np.asarray(generate_random_data(m, False)) #Generate random data
    Y = Y_.reshape(m, 480*4)
    return (X, Y)

def create_train_model(X, Y):
    #Training LSTM
    model = Sequential()
    model.add(LSTM(n_a, return_sequences=True, input_shape=(None, n_x)))
    model.add(LSTM(n_a, return_sequences=True))
    model.add(LSTM(n_a))
    model.add(Dense(480*4, activation="linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=['accuracy'])
    model.fit(X, Y, batch_size=2, epochs=10, shuffle=False)
    return model

(sleep_json, mbed_json) = fetch_data()
(X, Y) = create_vectors(sleep_json, mbed_json)
model = create_train_model(X, Y)
