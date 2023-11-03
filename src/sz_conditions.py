
class StorageTemperatureConditions:
    def __init__(self, 
            initial,  # Initial in Boxen
            melting,
            completeIce
            ):
        self.__initial = initial
        self.__melting = melting
        self.__completeIce = completeIce

    @property
    def initial(self):
        return self.__initial
    @property
    def melting(self):
        return self.__melting
    @property
    def completeIce(self):
        return self.__completeIce

class HeatExchangerConditions:
    def __init__(self, 
            delta_T  # Temperaturspreizung, Inlet-Outlet
            ):
        self.__delta_T = delta_T
    @property
    def delta_T(self):
        return self.__delta_T

class Time:
    def __init__(self, delta_t, N_t):
        self.__delta_t = delta_t
        self.__N_t = N_t
    @property
    def delta_t(self):
        return self.__delta_t
    @property
    def N_t(self):
        return self.__N_t
