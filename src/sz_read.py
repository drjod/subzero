
from sz_geometry import StorageGeometry
from sz_parameter import PhaseParameter, StorageParameter, HeatExchangerParameter
from sz_conditions import StorageTemperatureConditions, HeatExchangerConditions, Time
from sz_source_term import SourceTerm
from sz_heat_exchanger import HeatExchanger

import importlib.util
import sys
import numpy as np
import pandas as pd

def read_data(path):
    if path not in sys.path:
        sys.path.append(path)

    geometry = importlib.import_module("geometry")
    parameter = importlib.import_module("parameter")
    storage_control = importlib.import_module("storage_control")

    try:
        # lese header variablen
        file1 = open(path + "/" + storage_control.input_file, 'r')
        Lines = file1.readlines()
        headervariables = Lines[0].split()

        frame = pd.read_table(path + "/" + storage_control.input_file, delimiter='\s+')

        time_series = np.resize(np.zeros(frame[headervariables[0]].size * 4),
                                [frame[headervariables[0]].size, 4])

        time_unitfactor = {"s": 1, "h": 3600, "d": 86400, "y": 86400 * 3600}
        heat_exchange_unitfactor = {"W": 1, "kW": 1e3, "MW": 1e6}

        for ndx in range(int(time_series.size / 4)):
            time_series[ndx][0] = ((frame[headervariables[0]][ndx] - frame[headervariables[0]][0]) *
                                   time_unitfactor[storage_control.time_unit]) + storage_control.time_shift
            time_series[ndx][1] = storage_control.storage_control
            time_series[ndx][2] = (frame[headervariables[1]][ndx] * storage_control.heat_exchange_factor *
                                   heat_exchange_unitfactor[storage_control.heat_exchange_unit])
            time_series[ndx][3] = storage_control.temperature_condition

        print("read file ", storage_control.input_file, " - ", frame["Zeit"].size, " lines")
    except:
        time_series = storage_control.time_series
        print("read time series - ", int(time_series.size/4), " entries")

    storageGeometry = StorageGeometry(geometry.V,  # Volumen
                                      geometry.A,  # Austauschfläche
                                      geometry.d,  # Austauschlänge
                                      geometry.N_active  # Anzahl aktiver Boxen (Speicherumgebung)
                                      )


    storageTemperatureConditions = StorageTemperatureConditions(
        parameter.temperature_initial,  # Initial in Boxen
        parameter.temperature_melting,  # Schmelztemperatur
        parameter.temperature_completeIce  # Temperatur für komplette Vereisung
    )

    storageParameter = StorageParameter(
        parameter.storage_porosity,  # porosity
        PhaseParameter(parameter.storage_fluid_heatCapacity,
                         parameter.storage_fluid_density,
                         parameter.storage_fluid_conductivity),  # fluid  (capacity, density, conductivity)
        PhaseParameter(parameter.storage_ice_heatCapacity,
                         parameter.storage_ice_density,
                         parameter.storage_ice_conductivity),  # ice
        PhaseParameter(parameter.storage_solid_heatCapacity,
                         parameter.storage_solid_density,
                         parameter.storage_solid_conductivity),  # solid
        parameter.storage_latentHeat,  # Latente Wärme
        parameter.storage_icingCoefficient  # Vereisungskoeffizient
    )
    
    
    
    heatExchangerParameter = HeatExchangerParameter(
        parameter.heatExchanger_transmissivity,  # Wärmedurchgangskoeffizient, k * A_k
        parameter.heatExchanger_fluidHeatCapacity,  # Volumetr. Wärmekapazität
        parameter.heatExchanger_pipeDiameter,  # Rohrdurchmesser
        parameter.heatExchanger_numberOfPipes,  # Anzahl an Rohre in BHE, 2=2U
        parameter.heatExchanger_numberOfBHEs  # Anzahl an BHEs in Speicherbox
    )

    heatExchanger = HeatExchanger(heatExchangerParameter)
    time = Time(parameter.time_delta_t, parameter.time_numberOfSteps)

    return (storageGeometry, storageTemperatureConditions, storageParameter,
            heatExchanger, time, time_series)
