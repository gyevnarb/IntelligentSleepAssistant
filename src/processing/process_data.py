import perlin
import numpy as np
import matplotlib.pyplot as plt

def generate_temperature_data(tmin=15, tmax=22, imin=0, imax=24, d=1440):
    """
    Generates temperature data points with values from [tmin, tmax] and in the
    time interval [imin, imax]

    Returns: A numpy array of dimension (imax - imin)*d x 1
    """

    pnf = perlin.PerlinNoiseFactory(1, 5)
    noise = np.linspace(imin, imax, d, endpoint=False) / imax
    i = 0
    for p in noise:
        noise[i] = pnf(p)
        i = i + 1

    noise = np.abs(noise * tmax + tmax)
    #np.clip(noise, tmin, tmax, out=noise)
    return noise

ret = generate_temperature_data()
plt.plot(ret)
plt.ylabel('temperatures')
plt.show()
