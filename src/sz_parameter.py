
class PhaseParameter:
    def __init__(self,
                 capacity,  # J/kg/K
                 density,  # kg/m³
                 conductivity  # W/m/K
                 ):
        self.__capacity = capacity
        self.__density = density
        self.__conductivity = conductivity
    @property
    def capacity(self):
        return self.__capacity
    @property
    def density(self):
        return self.__density
    @property
    def conductivity(self):
        return self.__conductivity

class StorageParameter:
    def __init__(self,
                 porosity,
                 fluid, ice, solid,  # class PhaseParameter
                 latent_heat,  # J/kg
                 icing_coefficient  # K
                 ):
        self.__porosity = porosity

        self.__fluid = fluid
        self.__ice = ice
        self.__solid = solid
        # Vereisung
        self.__latent_heat = latent_heat
        self.__icing_coefficient = icing_coefficient

    @property
    def porosity(self):
        return self.__porosity
    @property
    def fluid(self):
        return self.__fluid
    @property
    def ice(self):
        return self.__ice
    @property
    def solid(self):
        return self.__solid
    @property
    def latent_heat(self):
        return self.__latent_heat
    @property
    def icing_coefficient(self):
        return self.__icing_coefficient

class HeatExchangerParameter:
    def __init__(self,
                 k_A_k,  # Wärmeübertragung ?
                 CV,  # Volumetr. Wärmekapazität des Sondenfluides, J/m³/K
                 pipe_d,  # Rohrdurchmesser für Sondenfluid, m
                 number_of_pipes,  # Rohre pro BHE, 2=2U
                 number_of_BHEs,  # BHEs in Speicher
                 min_flow,  # minimale Fliessrate
                 max_flow,  # maximale Fliessrate
                 min_exchange,  # minimale Wärmeübertragung
                 min_temperatureGap
                 ):
        self.__k_A_k = k_A_k
        self.__CV = CV
        self.__A = number_of_pipes * 3.14159 * (pipe_d/2)**2  # Querschnittsfläche für Strömung
        self.__number_of_BHEs = number_of_BHEs
        self.__min_flow = min_flow
        self.__max_flow = max_flow
        self.__min_exchange = min_exchange
        self. __min_temperatureGap = min_temperatureGap
    @property
    def k_A_k(self):
        return self.__k_A_k
    @property
    def CV(self):
        return self.__CV
    @property
    def A(self):
        return self.__A
    @property
    def number_of_BHEs(self):
        return self.__number_of_BHEs
    @property
    def min_flow(self):
        return self.__min_flow
    @property
    def max_flow(self):
        return self.__max_flow
    @property
    def min_exchange(self):
        return self.__min_exchange
    @property
    def min_temperatureGap(self):
        return self.__min_temperatureGap