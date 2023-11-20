import pandas as pd
import sys
import importlib
import time

if "src" not in sys.path:
    sys.path.append("src")

from subzero import SubZero

path = "examples/gews_2"

time0 = time.perf_counter()
subzero = SubZero(path)
time1 = time.perf_counter()
subzero.calculate()
time2 = time.perf_counter()

print("Setup time (s): {}".format(time1-time0))
print("Simulation time (s): {}".format(time2-time1))

########################
# PLOTTING

if True:

    plots = ["temperatur_speicher", "temperatur_aussen", "waernme",
             "eisfraktion", "raten", "fluidgeschwindigkeit", "flag"]
    plots_shown = {
        "temperatur_speicher": 1,
        "temperatur_aussen": 0,
        "waernme": 0,
        "eisfraktion": 0,
        "raten": 1,
        "fluidgeschwindigkeit": 1,
        "flag": 1
    }

    datum = False

    anzahl_plots = 0
    for key in plots:
        if plots_shown[key] == 1:
            anzahl_plots += 1

    import numpy as np
    import matplotlib.pyplot as plt
    import datetime as dt
    import matplotlib.dates as mdates
    from matplotlib.dates import WeekdayLocator
    # import constants for the days of the week
    from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
    # from matplotlib.dates import HourLocator, DayLocator, YearLocator
    from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

    time_array = subzero.time_array_shifted_to_loadcurve

    if datum:
        date_start = dt.datetime(1900,  # year
                                 1,  # month
                                 1,  # day
                                 0,  # hour
                                 0,  # min
                                 0  # sec
                                 )

        x = [date_start + dt.timedelta(seconds=int(time)) for time in time_array]  # x-achse
        # loc_major = WeekdayLocator(byweekday=(MO)) # für major Grid, ausgewhälter Wochentag
        # loc_minor = AutoMinorLocator(7) # für minot Grid, einzelne Tage
        date_format = mdates.DateFormatter('%d.%m.')
        labelrotation = 90  # grad, für x-label (Datum)

    else:
        x = subzero.time_array_shifted_to_loadcurve / 86400 / 365

    fig, axes = plt.subplots(anzahl_plots, 1, figsize=(25, 20))
    plt.subplots_adjust(wspace=.3, hspace=.5)
    ndx = 0
    if plots_shown["temperatur_speicher"]:
        ax = axes[ndx]
        ax.set_title("Temperaturen im Speicher (Box 0)")
        ax.plot(x, subzero.T[:, 0], label='Box 0', color='red')  # , marker='x')
        ax.plot(x[1:], subzero.T_in[1:], label='T_in', color='orange')
        ax.plot(x[1:], subzero.T_out[1:], label='T_out', color='brown')

        try:
            if path not in sys.path:
                sys.path.append(path)
            storage_control = importlib.import_module("storage_control")

            frame = pd.read_excel(path + "/" + storage_control.input_file)
            ax.plot(x[1::12], frame.T_Storage, label='T_Storage', color='black', linestyle='--')
        except:
            pass

        ax.set_ylabel("T [°C]")
        #ax.set_ylim([-.1, .1])

        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)
        # ax.set_xticklabels([])
        ax.legend()  # loc='lower right')
        ndx += 1
    #####################

    if plots_shown["temperatur_aussen"]:
        ax = axes[ndx]
        ax.set_title("Temperaturen außerhalb des Speichers (Boxen 1-12)")
        ax.plot(x, subzero.T[:, 1], label='Box 1 - unterhalb', color='blue')
        ax.plot(x, subzero.T[:, 2], label='Box 2 - seitlich', color='green')
        ax.plot(x, subzero.T[:, 7], label='Box 7 - weit unten', color='blue', linestyle='--')
        ax.plot(x, subzero.T[:, 8], label='Box 8 - weit seitlich', color='green', linestyle='--')

        ax.set_ylabel("T [°C]")
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)

        # ergänze ergebnisse aus excelfile
        try:
            if path not in sys.path:
                sys.path.append(path)
            storage_control = importlib.import_module("storage_control")

            frame = pd.read_excel(path + "/" + storage_control.input_file)

            ax.plot(x[1::12], frame.T_UD, label='T_UD', color='black', linestyle='--')
        except:
            pass

        ax.legend()  # loc='lower right')
        ndx += 1
    #########################

    if plots_shown["waernme"]:
        storage_factor = 1e6 * 3600
        ax = axes[ndx]
        ax.set_title("Wärme in Boxen")
        ax.plot(x, subzero.H[:, 0] / storage_factor, label='Box 0', color='red')
        ax.plot(x, subzero.H[:, 1] / storage_factor, label='Box 1', color='blue')
        ax.plot(x, subzero.H[:, 2] / storage_factor, label='Box 2', color='green')
        ax.plot(x, subzero.H[:, 7] / storage_factor, label='Box 7', color='blue', linestyle='--')
        ax.plot(x, subzero.H[:, 8] / storage_factor, label='Box 8', color='green', linestyle='--')

        ax.set_ylabel("[MWh]")
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)

        ax.legend()  # loc='lower right')
        ndx += 1
    #########################

    if plots_shown["eisfraktion"]:
        ax = axes[ndx]
        ax.set_title("Eisfraktion")
        ax.plot(x[1:], 1 - subzero.theta[1:], color='red')

        ax.set_ylabel("[-]")
        ax.set_ylim([-0.1, 1.1])
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)
        ndx += 1

    #########################

    if plots_shown["raten"]:
        storage_factor = 1e3
        V_box0 = 4 * 4 * 6  # m3
        ax = axes[ndx]
        ax.set_title("Speicherraten")
        ax.plot(x, subzero.Q_ext / storage_factor,
                label='Angeforderte Be- und Entlandung', color='orange')
        ax.plot(x, subzero.Q / storage_factor,
                label='Tatsächliche Be- und Entlandung', color='red')
        ax.plot(x,
                -subzero.latent_heat_capacity * V_box0 *
                (subzero.T[:, 0] - np.roll(subzero.T[:, 0], 1)) / 3600 / storage_factor,
                label='Latente Wärme', color='blue', linestyle='--')

        #ax.set_ylim([-.1, .1])
        ax.set_ylabel("[KW]")
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)
        ax.legend()  # loc='lower right')
        ndx += 1

    #########################

    if plots_shown["fluidgeschwindigkeit"]:
        ax = axes[ndx]
        ax.set_title("Fliessrate in Wärmetauscher")
        #ax.plot(x[1:], subzero.v[1:], label='v', color='orange')
        ax.plot(x[1:], subzero.Q_flow[1:], label='v', color='orange')
        #ax.set_ylim([-5, 0])

        ax.set_ylabel("[m/s]")
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)
        # ax.legend()#loc='lower right')
        ndx += 1

    #########################

    if plots_shown["flag"]:
        ax = axes[ndx]
        ax.set_title("Flag für Wärmetauscher")
        ax.plot(x[1:], subzero.heat_exchanger_flag[1:], label='flag', color='orange')

        ax.set_ylabel("[-]")
        if datum:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO)))  # mdates.DayLocator(interval=1))
            ax.tick_params(axis='x', labelrotation=labelrotation)
            ax.xaxis.set_minor_locator(AutoMinorLocator(7))
        ax.minorticks_on()
        ax.grid(visible=True, which='major', linestyle='-', linewidth=1.)
        ax.grid(visible=True, which='minor', linestyle='--', linewidth=.5)
        # ax.legend()#loc='lower right')
        ndx += 1

    plt.show()
