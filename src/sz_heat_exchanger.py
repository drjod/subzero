import numpy as np

from sz_heat_exchanger_control import Control_Delta, Control_in, Control_out

class HeatExchangerValues:
    __delta_T = float()
    __T_in = float()
    __T_out = float()
    __Q = float()
    __Q_flow = float()

    def __init__(self):
        self.__flag = 1  # aktiv gesetzt (und kein Error)
    @property
    def delta_T(self):
        return self.__delta_T
    @property
    def T_in(self):
        return self.__T_in
    @property
    def T_out(self):
        return self.__T_out
    @property
    def Q(self):
        return self.__Q
    @property
    def Q_flow(self):
        return self.__Q_flow
    @property
    def flag(self):
        return self.__flag
    @delta_T.setter
    def delta_T(self, value):
        self.__delta_T = value
    @T_in.setter
    def T_in(self, value):
        self.__T_in = value
    @T_out.setter
    def T_out(self, value):
        self.__T_out = value
    @Q.setter
    def Q(self, value):
        self.__Q = value
    @flag.setter
    def flag(self, value):
        self.__flag = value
    @Q_flow.setter
    def Q_flow(self, value):
        self.__Q_flow = value
class HeatExchanger:
    __control = int()

    def __init__(self,
                 heatExchangerParameter
                 # , heatExchangerConditions
                 ):
        self.__parameter = heatExchangerParameter
        self.__values = HeatExchangerValues()
        self.__flag = 1  # aktiv gesetzt (und kein Error)
        #self.__conditions = heatExchangerConditions

    @property
    def values(self):
        return self.__values
    @property
    def control(self):
        return self.__control
    def configure(self, storage_control):

        if abs(storage_control[0]) == 1:
            self.__control = Control_Delta(storage_control[1],  # Wärmeaustausch (Speicheranforderung) [W]
                                           storage_control[2],  # fixe Temperaturspreizung [K]
                                           self.__parameter.k_A_k, self.__parameter.number_of_BHEs)
            #self.__values.delta_T = storage_control[2]
        elif abs(storage_control[0]) == 2:
            self.__control = Control_in(storage_control[1],  # Wärmeaustausch (Speicheranforderung) [W]
                                        storage_control[2],   # fixe Temperatur am Einlass [°C]
                                        self.__parameter.k_A_k, self.__parameter.number_of_BHEs)
            #self.__values.T_in = storage_control[2]
        elif abs(storage_control[0]) == 3:
            self.__control = Control_out(storage_control[1],  # Wärmeaustausch (Speicheranforderung) [W]
                                         storage_control[2],  # fixe Temperatur am Auslass [°C]
                                         self.__parameter.k_A_k, self.__parameter.number_of_BHEs)
            #self.__values.T_out = storage_control[2]

        if storage_control[0] > 0:
            self.__values.Q = storage_control[1]
        else:
            self.__values.Q_flow = storage_control[1]


    def calculate_Q(self, T_HE, T_S):
        # Wärmefluss Sondenfluid <-> Untergrund (W)
        return self.__parameter.k_A_k * self.__values.delta_T / np.log((T_HE - T_S) /
                                                                             (T_HE-self.__values.delta_T - T_S))

    #def __f(self, T, T_S):
    #
    #    return self.__values.Q - self.calculate_Q(T, T_S)

    #def __deriv_f(self, T_HE, T_S):
    #    factor = (self.__parameter.k_A_k * self.__values.delta_T /
    #                 (np.log((T_HE - T_S) / (T_HE - self.__values.delta_T - T_S)))**2)
    #    term_0 = (T_HE - T_S)**(-1)
    #    term_1 = - (T_HE - self.__values.delta_T - T_S)**(-1)
    #    deriv_f = factor * (term_0 + term_1)
    #    return deriv_f

    def calculate(self, T_S):
        # Newton-Iteration
        T = self.__control.iteration_start_value(T_S)

        #print('Q: ', self.__control.heat_exchange(), ' T_fix: ', self.__control.temperature_fix(), ' T_S: ', T_S, ' T_var: ', T)
        ndx_max = 10  # Anzahl an Maximaliterationen
        for ndx in range(ndx_max):
            _T = T - self.__control.f(T, T_S) / self.__control.deriv_f(T, T_S)
            self.__values.T_in, self.__values.T_out, self.__values.delta_T = self.__control.update(_T)
            self.__values.flag = self.__control.flag
            #print(self.__values.T_in, self.__values.T_out, self.__values.delta_T, T_S)
            #print("velocity: ", self.v())
            #print(ndx, ", T_var: ",  _T)
            #if abs(self.v()) > 1:
            #    self.__control.Q(self.__control.heat_exchange() / 2)
            #    print("Q reduced")
            if abs(_T - T) < 0.01:  # Fehlertoleranz
                break
            if ndx == ndx_max-1:
                print("WARNUNG - Maximalanzahl an Newton-Iterationen erreicht - Fehler (K): ",  abs(_T - T))
                self.__values.flag = -1

            T = _T

        #if abs(self.v()) > 5:
        #    Q, _T = self.__control.reduce_heat_exchange(T_S)
        #    print("Velocity ", self.v(), " > 5 : Heat exhcange reduded to ", Q)
        # In Newton iteration zum Anpassen von Speicherraten
        # self.__values.T_in, self.__values.T_out, self.__values.delta_T = self.__control.update(_T)

    def v(self):
        # Fluidgeschwindigkeit is Sonde (postprocessing)
        return self.__values.Q / self.__parameter.A / self.__parameter.CV / self.__values.delta_T
