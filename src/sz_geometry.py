
class StorageGeometry:
    # Konstruktor
    def __init__(self,
                 V,  # Volumen, N-Array, N: Anzahl an Boxen
                 A,  # Austauschfläche, NxN-Matrix
                 d,  # Austauschlänge, NxN-Matrix
                 N_active  # Anzahl aktiver Boxen, Temperatur,  Wärmezunahme wird berechnet für die Boxen [: N_active]
                 ):
        self.__N = V.size # Anzahl an Boxen
        self.__V = V
        self.__A = A
        self.__d = d
        self.__N_active = N_active
    # getter
    @property
    def N(self):
        return self.__N
    @property
    def V(self):
        return self.__V
    @property
    def A(self):
        return self.__A
    @property
    def d(self):
        return self.__d
    @property
    def N_active(self):
        return self.__N_active
