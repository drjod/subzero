import numpy as np

# Temperaturbedingungen -> class StorageTemperatureConditions

temperature_initial = 10.  # Initialtemperatur für gesamten Untergrund [°C], konstante Randbedingung, wenn Box inaktiv
temperature_melting = 0.  # Schmelztemperatur [°C]
temperature_completeIce = -4.  # Temperatur für komplette Vereisung [°C]

# Wärmetauscherparameter
# -> class HeatExchangerConditions
# heatExchanger_temperatureSpread = 3.  # Temperaturspreizung Eintritt / Austritt [K]
# -> class HeatExchangerParameter (2U- BHEs)
heatExchanger_transmissivity = 40  # Wärmedurchgangszahl (k, W/m²/K) x Austauschfläche, [W/K]
heatExchanger_fluidHeatCapacity = 4.2e6  # Volumetrische Wärmekapazität des Sondenfluides [J/m³/K]
heatExchanger_pipeDiameter = .025  # Rohrdurchmesser [m]
heatExchanger_numberOfPipes = 2  # Anzahl an Rohren in BHE, 2 = 2U
heatExchanger_numberOfBHEs = 16 # Anzahl an BHEs in Speicherbox

heatExchanger_minFlow = 0.0001 # Minimale Fliessrate [m³/s]
heatExchanger_maxFlow = 0.001 # Maximale Fliessrate [m³/s]
heatExchanger_minExchange = 3000 # minimale Wärmeübertragung [W]
heatExchanger_minTemperatureGap = 3 # Minimaler Temperaturunterschied zwischen Wärmetauscher am Zufluss und Speicher (box 0) [K]



# Speicherparameter -> class StorageParameter
storage_porosity = 0.35  # Porosität des Untergrundes [-]
storage_latentHeat = 3e5  # Latente Wärme des Phasenüberganges flüssig / fest [J/kg]
storage_icingCoefficient = 1.  # c aus theta = exp( -[(T-T_m) /c]^2 ), (T_m: Schmelztemperatur) [K]

# Speicherparameter -> class PhaseParameter
# Fluid
storage_fluid_heatCapacity = 4200.  # Spezifische Wärmekapazizät [J/kg/K]
storage_fluid_density = 1000.  # Dichte [kg/m³]
storage_fluid_conductivity = .6  # Wärmeleitfähigkeit [W/m/K]
# Eis
storage_ice_heatCapacity = 2000.  # Spezifische Wärmekapazizät [J/kg/K]
storage_ice_density = 920.  # Dichte [kg/m³]
storage_ice_conductivity = 2.  # Wärmeleitfähigkeit [W/m/K]
# Festphase
storage_solid_heatCapacity = 2700.  # Spezifische Wärmekapazizät [J/kg/K]
storage_solid_density = 700.  # Dichte [kg/m³]
storage_solid_conductivity = 4.2  # Wärmeleitfähigkeit [W/m/K]


# Zeitschritte -> class Time
time_delta_t = 3600 #   15768  # Zeitschrittweite [s]
time_numberOfSteps = 1992 # 1889  # 1888   # Anzahl an Zeitschritten

# Quellterm für Speicher (Box 0) -> class SourceTerm, Stufenfunktion (psoitiv, negativ im Wechsel)
sourceTerm_cycleDuration = 31536000  # Zyklusdauer [s]
sourceTerm_value = -3600  # Belade- und Entladerate[W], Positiv: Start mit Wärmebeladung


