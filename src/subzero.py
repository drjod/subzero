
import numpy as np
import sz_read

# Speichermodell
# Ergebnisse in Member-Variablen für alle N_t Zeitschritte
#     T:     Temperatur, (N*N_t+1)-Matrix
#     Q_int: Interne Wärmeflüsse, (N*N*N_t+1)-Matrix
# Anfangswerte: T[0], Q_int[0]


class SubZero:
    def __init__(self,
                 _path,  # Pfad zu Verzeichnis mit Inputdateien (geometry.py, parameter.py)
                 output=True
                 ):

        (self.__storageGeometry, self.__storageTemperatureConditions, self.__storageParameter,
         self.__heatExchanger,
         self.__time, self.__storage_control_time_series) = sz_read.read_data(_path)

        N = self.__storageGeometry.V.size
        self.__output = output
        ### Ergebnisse
        # Temperatur T: (N_t+1 * N)-Matrix, initialisiert (komplett) mit Anfangstemperatur
        # Interne Flüße Q_int: (N_t+1 * N * N)-Tensor, initialisiert mit 0
        self.__T = np.resize(np.ones(N * self.__time.N_t+1)*self.__storageTemperatureConditions.initial,
                           (self.__time.N_t+1, N))
        self.__Q_int = np.resize(np.zeros(N * N * self.__time.N_t+1), (self.__time.N_t+1, N, N))
        self.__Q_ext = np.zeros(self.__time.N_t+1)
        # Wasserfraktion
        self.__theta = -np.ones(self.__time.N_t+1)
        # Wärmetauscher
        self.__T_in = np.zeros(self.__time.N_t+1)  # Berechnet für [1:] (T_in[0] bleibt 0)
        self.__T_out = np.zeros(self.__time.N_t+1)  # Berechnet für [1:] (T_out[0] bleibt 0)
        self.__v = np.zeros(self.__time.N_t + 1)  # Berechnet für [1:] (v[0] bleibt 0)
        self.__Q = np.zeros(self.__time.N_t + 1)  # Tatsächlicher Wärmeaustausch
        self.__Q_flow = np.zeros(self.__time.N_t + 1)  # Berechnet für [1:] (v[0] bleibt 0)
        self.__heat_exchanger_flag = -np.ones(self.__time.N_t + 1)
        # Volumetrische Wärmekapazität für Phasenwechsel [W/m³/K]
        self.__latent_heat_capacity = np.zeros(self.__time.N_t+1)
        # Wärmeinhalt in Boxen [Ws], (N*N_t+1)-Matrix
        self.__H = np.resize(np.zeros(N * self.__time.N_t+1), (self.__time.N_t+1, N))
        # Wärmeinhalt in Untergrund [Ws]
        self.H_total = np.zeros(self.__time.N_t+1)
        self.__time_shift_input = 0

        self.__time_array = np.array(range(0, self.__time.N_t + 1)) * self.__time.delta_t
    @property
    def T(self):
        return self.__T
    @property
    def Q_int(self):
        return self.__Q_int
    @property
    def Q_ext(self):
        return self.__Q_ext
    @property
    def H(self):
        return self.__H
    @property
    def T(self):
        return self.__T
    @property
    def T_in(self):
        return self.__T_in
    @property
    def T_out(self):
        return self.__T_out
    @property
    def v(self):
        return self.__v
    @property
    def Q(self):
        return self.__Q
    @property
    def Q_flow(self):
        return self.__Q_flow
    @property
    def heat_exchanger_flag(self):
        return self.__heat_exchanger_flag
    @property
    def time(self):
        return self.__time
    @property
    def latent_heat_capacity(self):
        return self.__latent_heat_capacity
    @property
    def storageGeometry(self):
        return self.__storageGeometry
    @property
    def theta(self):
        return self.__theta
    @property
    def heatExchanger(self):
        return self.__heatExchanger
    @property
    def time_array_shifted_to_loadcurve(self):
        return self.__time_array + self.__time_shift_input

    def calculate(self):
        self.__time_shift_input = self.__storage_control_time_series[0][0] - self.__time.time_shift
        #print(self.storageGeometry.N_active)
        for n_T in range(1, self.__time.N_t+1):

            if self.__output:
                print("Timestep {} - {} s - {:.2} d".format(
                    n_T, self.__time_array[n_T], self.__time_array[n_T]/86400))
            #### Berechne Temperatur für aktive Boxen

            # Kopiere Temperatur und Wärmeinhalt von letztem Zeitschritt, für alle aktiven Boxen
            self.__T[n_T, :self.__storageGeometry.N_active] = self.__T[n_T-1, :self.__storageGeometry.N_active]
            self.__H[n_T, :self.__storageGeometry.N_active] = self.__H[n_T-1, :self.__storageGeometry.N_active]

            self.__theta[n_T] = self._theta(self.__T[n_T-1, 0])  # Wasserfraktion in Speicher, Box 0

            self.__latent_heat_capacity[n_T] = self._latent_heat_capacity(self.__T[n_T-1,  # explicit
                                                                                     0  # storage, box 0
                                                                                     ])
            # Addiere externen Quell- und Senkenterm, für Speicher (Box 0)
            storage_control = (self.__storage_control_time_series[self.__storage_control_time_series[:, 0] >=
                                                                  self.__time_array[n_T]+self.__time_shift_input][0])

            self.__Q_ext[n_T] = storage_control[2]
            if self.__Q_ext[n_T] != 0:
                if self.__output:
                    if storage_control[1] == 1:
                        temperature_unit, temperature_given = 'K', 'DT'
                    elif storage_control[1] == 2:
                        temperature_unit, temperature_given = '°C', 'T_in'
                    elif storage_control[1] == 3:
                        temperature_unit, temperature_given = '°C', 'T_out'
                    else:
                        print("ERROR - storage model {} not supported", format(storage_control[1]))

                    print("\tQ: {:.2} W - {}: {:.2} {}".format(storage_control[2], temperature_given,
                                                               storage_control[3], temperature_unit))
                # Leistung angefragt
                self.__heatExchanger.configure(storage_control[1:])

                self.__heatExchanger.calculate(
                    self.__T[n_T-1,
                             0  # Speicher, Box 0
                             ],
                    self.__output)
                if self.__output:
                    print("capacity: ", self.heat_capacity(self.__T[n_T, 0]), "  for T_S: ", self.__T[n_T, 0])
                    print("\t-> v: {:.3} m/s".format(self.__heatExchanger.v()))

                self.__T_in[n_T], self.__T_out[n_T] = (self.__heatExchanger.values.T_in,
                                                       self.__heatExchanger.values.T_out)
                self.__v[n_T] = self.__heatExchanger.v()
                self.__Q_flow[n_T] = self.__heatExchanger.Q_flow()
                self.__Q[n_T] = self.__heatExchanger.values.Q
                self.__heat_exchanger_flag[n_T] = self.__heatExchanger.values.flag

                # H_ext = storage_control[2] * self.__time.delta_t # self.__sourceterm(n_T) * self.__time.delta_t
                ############### #H_ext = self.__heatExchanger.control.heat_exchange() * self.__time.delta_t
                H_ext = self.__heatExchanger.values.Q * self.__time.delta_t
            else:
                if self.__output:
                    print("\tQ: 0 W")
                # Keine Leistung angefragt
                self.__T_in[n_T], self.__T_out[n_T], self.__heat_exchanger_flag[n_T], self.__v[n_T], H_ext = (
                    float("nan"), float("nan"), 0, 0., 0.)

            self.__T[n_T, 0] += (H_ext /
                                 (self.heat_capacity(self.T[n_T-1, 0]) - self.__latent_heat_capacity[n_T]) /
                                 self.__storageGeometry.V[0])
            self.__H[n_T, 0] += H_ext
            self.H_total[n_T] = self.H_total[n_T-1] + H_ext

            for n_0 in range(self.__storageGeometry.N_active):
                for n_1 in range(self.__storageGeometry.N):
                    #### Berechne interne Quell- und Senkenterme
                    # Arithmetischer Mittelwert für Wärmeleitfähigkeit
                    heat_conductivity = (self.heat_conductivity(self.__T[n_T-1, n_0]) +
                                          self.heat_conductivity(self.__T[n_T-1, n_1])) / 2
                    self.__Q_int[n_T, n_0, n_1] = ((self.__T[n_T-1, n_1] - self.__T[n_T-1, n_0]) * heat_conductivity *
                                                   self.__storageGeometry.A[n_0][n_1] /
                                                   self.__storageGeometry.d[n_0][n_1])

                    # Addiere interne Quell- und Senkenterme -> Ergebnis
                    H_int = self.__Q_int[n_T, n_0, n_1] * self.__time.delta_t
                    self.__H[n_T, n_0] += H_int
                    if n_0 == 0:  # Speicher
                        self.__T[n_T, 0] += (H_int /
                                             (self.heat_capacity(self.T[n_T-1, 0]) -
                                              self.__latent_heat_capacity[n_T]) /
                                             self.__storageGeometry.V[0])

                        # print("heat capacity: ", self.heat_capacity(self.T[n_T-1, 0]))
                    else:
                        self.T[n_T, n_0] += (H_int /
                                             self.heat_capacity(self.__T[n_T-1, n_0]) /
                                             self.__storageGeometry.V[n_0])

    def _theta(self, T):
        return np.exp(-((T - self.__storageTemperatureConditions.melting) /
                        self.__storageParameter.icing_coefficient)**2
                      ) if (T < self.__storageTemperatureConditions.melting) else 1.

    def deriv_theta(self, T):
        return (-self._theta(T) * 2 * (T - self.__storageTemperatureConditions.melting) /
                self.__storageParameter.icing_coefficient**2)

    def _latent_heat_capacity(self, T):  # Volumetrische Wärmekapazität für Phasenwechsel [W/m³/K]
        if T > self.__storageTemperatureConditions.melting or T < self.__storageTemperatureConditions.completeIce:
            return 0
        else:
            return (-self.deriv_theta(T) * self.__storageParameter.latent_heat *
                    self.__storageParameter.porosity * self.__storageParameter.ice.density)

    def heat_capacity(self, T):  # Volumetrische Wärmekapazität [W/m³/K]
        theta = self._theta(T)
        term_fluid = (self.__storageParameter.fluid.capacity *
                      self.__storageParameter.fluid.density * self.__storageParameter.porosity * theta)
        term_ice = (self.__storageParameter.ice.capacity *
                    self.__storageParameter.ice.density * self.__storageParameter.porosity * (1 - theta))
        term_solid = (self.__storageParameter.solid.capacity *
                      self.__storageParameter.solid.density * (1 - self.__storageParameter.porosity))

        return term_fluid + term_ice + term_solid

    def heat_conductivity(self, T):  # Wärmeleitfähigkeit [W/m/K]
        theta = self._theta(T)
        term_fluid = self.__storageParameter.fluid.conductivity * self.__storageParameter.porosity * theta
        term_ice = self.__storageParameter.ice.conductivity * self.__storageParameter.porosity * (1. - theta)
        term_solid = self.__storageParameter.solid.conductivity * (1. - self.__storageParameter.porosity)
        return term_fluid + term_ice + term_solid
