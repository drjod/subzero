import numpy as np
# Festlegung von
# V: Boxvolumen [m³]
# A: Fläche zwischen Boxen [m²], Box i, j sind gekoppelt wenn A[i, j] != 0
# d: Austauschlänge [m]
# N_Active: Anzahl aktiver Boxen. Temperatur, Wärmezunahme wird berechnet für die Boxen [: N_active]

V = np.array([96.,  # Speicher, 4x4x6 m
              156., 198., 156., 198., 198., 198.,  # Speicherumgebung ,10x10x12  m (6 Boxen, 1, 3 : unten & oben, 2, 4, 5, 6: seitlich)
              1000000., 1000000., 1000000., 1000000., 1000000., 1000000.  # entfernterer Außenbereich (6 Boxen)
              ])

N = V.size
N_active = N  # 7 (ohne entfernten Außenbereich)

A = np.resize(np.zeros(N*N), (N, N))  # 9x9-Matrix, gefüllt mit 0
d = np.resize(np.ones(N*N), (N, N))  # 9x9-Matrix, gefüllt mit 1

# Kopplung Speicher <-> Speicherumgebung
for ndx in [1, 3]:  # unten & oben
    A[0, ndx] = 16.  # 4x4 m²
    A[ndx, 0] = 16.
for ndx in [2, 4, 5, 6]:  # seitlich
    A[0, ndx] = 24.  # 4x6 m²
    A[ndx, 0] = 24.
    
for ndx in range(1, 7):
    d[0, ndx] = 1.9
    d[ndx, 0] = 1.9

# Kopplung Speicherumgebung <-> entfernterer Außembereich
for ndx in [1, 3]:  # unten & oben
    A[ndx, ndx+6] = 100.  # 10x10 m²
    A[ndx+6, ndx] = 100.

for ndx in [2, 4, 5, 6]:  # seitlich
    A[ndx, ndx+6] = 120.  # 10x12 m²
    A[ndx+6, ndx] = 120.

for ndx in range(1, 7):
    d[ndx, ndx+6] = 6.6
    d[ndx+6, ndx] = 6.6
