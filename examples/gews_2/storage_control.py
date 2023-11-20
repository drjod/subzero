import numpy as np

time_shift = 0


time_series = np.array([
    [1. * 864000*2, 2, -3600, 3],
    [1. * 864000*10, 2, -3600, 0],  # Zeit, modus, Rate [W], Temperatur [°C]
    [2. * 864000*10, 2, 3600, 15],
    [3. * 864000*10, 2, -3600, 0],
    [4. * 864000*10, 2, 3600, 10]
])
