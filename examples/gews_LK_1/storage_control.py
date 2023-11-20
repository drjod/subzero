

input_file = "input.txt"
time_unit="d"   # [s]econd, [h]our, [d]ay, [y]ear
time_shift = 3600  # Damit Leistungskurve konsistent mit Zeitschrittsteuerung ist (Quellterm implizit im Modell). 
heat_exchange_unit = "kW"  # W, kW, MW
heat_exchange_factor =    -1/2.5  # Im Modell ist positive Leistung Wärmezugabe

storage_control = 1 # modus für temperaturvorgabe, 1: delta_T, 2: T_in, 3: T_out 
temperature_condition = 3 # wert für temperaturvorgabem, hier Temperaturspreizung (modus 1)
