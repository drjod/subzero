import numpy as np

# Given: delta_T, Q
# Calculated: T_in

class Control_Delta:
    def __init__(self, Q, T_fix, k_A_k, n_BHEs):
        self.__Q = Q
        self.__T_fix = T_fix  # T_delta
        self.__k_A_k = k_A_k
        self.__n_BHES = n_BHEs
        self.__flag = 1
    @property
    def flag(self):
        return self.__flag
    def temperature_var(self, values):
        return values.T_in
    def temperature_fix(self):
        return self.__T_fix
    def heat_exchange(self):
        return self.__Q
    def iteration_start_value(self, T_S):
        return T_S + 10 if self.__Q > 0 else T_S - 10

    def f(self, T_var, T_s):
        try:
            f = (self.__Q / self.__n_BHES - self.__k_A_k * self.__T_fix /
                 np.log((T_var - T_s) / (T_var - self.__T_fix - T_s)))
        except:
            self.__flag = -2
            f = 0
            print("WARNING - Error in Log calculation")

        return 0
    def deriv_f(self, T_var, T_s):
        try:
            factor = (self.__k_A_k * self.__T_fix /
                      (np.log((T_var - T_s) / (T_var - self.__T_fix - T_s)))**2)
        except:
            self.__flag = -2
            factor = 1
            print("WARNING - Error in Log calculation")

        term_0 = (T_var - T_s)**(-1)
        term_1 = - (T_var - self.__T_fix - T_s)**(-1)

        return factor * (term_0 + term_1)

    def update(self, T_var):
        return (T_var,
                T_var - self.__T_fix if self.__Q > 0 else T_var + self.__T_fix,
                self.__T_fix
                )

# Given: T_in, Q
# Calculated: T_out
class Control_in:
    def __init__(self, Q, T_fix, k_A_k, n_BHEs):
        self.__Q = Q
        self.__T_fix = T_fix  # T_in
        self.__k_A_k = k_A_k
        self.__n_BHES = n_BHEs
        self.__flag = 1
    @property
    def flag(self):
        return self.__flag
    def temperature_var(self, values):
        return values.T_out
    def temperature_fix(self):
        return self.__T_fix
    def heat_exchange(self):
        return self.__Q
    def iteration_start_value(self, T_S):
        return (T_S + self.__T_fix * 3) / 4

    def Q(self, value):
        self.__Q = value

    def f(self, T_var, T_s):
        #print("T_fix: ", self.__T_fix, ", T_var: ", T_var, ", T_s: ", T_s)
        #print("log: ", np.log((self.__T_fix - T_s) / (T_var - T_s)))
        #if self.__Q < 0 and self.__T_fix > T_var:
        #    self.__Q /= 2
        #if self.__Q > 0 and self.__T_fix < T_var:
        #    self.__Q /= 2
        #if abs(self.__T_fix - T_s) < 1:
        #    self.__Q = 0
        #    return 0
        #if abs(self.__T_fix - T_var) < 1:
        #    self.__Q /= 2
        return (self.__Q / self.__n_BHES - self.__k_A_k * (self.__T_fix - T_var) /np.log((self.__T_fix - T_s) / (T_var - T_s)))

    def deriv_f(self, T_var, T_s):
        factor_0 = self.__k_A_k / np.log((self.__T_fix - T_s) / (T_var - T_s))
        factor_1 = 1 - (np.log((self.__T_fix - T_s)/(T_var - T_s)))**(-1) * (self.__T_fix - T_var)/(T_var - T_s)
        return factor_0 * factor_1

    def update(self, T_var):
        return (self.__T_fix,
                T_var,
                self.__T_fix - T_var if self.__Q > 0 else T_var - self.__T_fix
                )

    #def reduce_heat_exchange(self, T_S):
    #    v_max = 5
    #    A = 16*3.14159 * (.025/2)**2
    #    T_out = T_S + (self.__T_fix - T_S) / np.exp(self.__k_A_k *A / v_max / 4.2e6)
    #    self.__Q = v_max * A * 4.2e6 *(self.__T_fix - T_out)
    #    return T_out

# Given: T_out, Q
# Calculated: T_in

class Control_out:
    def __init__(self, Q, T_fix, k_A_k, n_BHEs):
        self.__Q = Q
        self.__T_fix = T_fix  # T_out
        self.__k_A_k = k_A_k
        self.__n_BHES = n_BHEs

    def temperature_var(self, values):
        return values.T_in

    def temperature_fix(self):
        return self.__T_fix

    def heat_exchange(self):
        return self.__Q

    def iteration_start_value(self, T_S):
        return (T_S + self.__T_fix) / 2

    def f(self, T_var, T_s):
        _log = np.log((T_var - T_s) / (self.__T_fix - T_s))
        print('log: ', _log)
        _f = self.__Q - self.__k_A_k * (T_var - self.__T_fix) / np.log((T_var - T_s) / (self.__T_fix - T_s))
        print('f: ', _f)
        return _f

    def deriv_f(self, T_var, T_s):
        _log = np.log((T_var - T_s) / (self.__T_fix - T_s))
        #print('log: ', _log)
        factor_0 = self.__k_A_k / _log
        factor_1 =  (T_var - self.__T_fix)/(T_var - T_s)/_log - 1

        return factor_0 * factor_1


    def update(self, T_var):
        return T_var, self.__T_fix, T_var - self.__T_fix