import pandas as pd
import numpy as np
import d_setting
import d_config
from d_model import main
from d_solar import calc_solar_irradiance
from d_offrace_solarcalc import calculate_energy

df_list = []
T = d_setting.RaceEndTime - d_setting.RaceStartTime -  2 * d_setting.Control_stop_time
day_counter = 1
time_counter = 0
CONTROL_STOP_DURATION = 30 * 60

# for i in range(10):
    # if i % 2 == 0:
    #     d_setting.set_day_state(day_counter, i, time_counter)
    #     d_setting.InitialBatteryCapacity = min(d_config.BATTERY_CAPACITY, stop_gain + d_setting.InitialBatteryCapacity)
    #     outdf, timetaken = main(d_setting.route_df)
    #     df_list.append(outdf)

    #     time_counter += timetaken
    #     stop_gain = calculate_energy(time_counter, time_counter + CONTROL_STOP_DURATION)
    #     time_counter += CONTROL_STOP_DURATION

    # else:
    #     # d_setting.set_day_state(day_counter, i, time_counter)
    #     # d_setting.InitialBatteryCapacity = min(d_config.BATTERY_CAPACITY, stop_gain + d_setting.InitialBatteryCapacity)

    #     outdf, timetaken = main(d_setting.route_df)

    #     df_list.append(outdf)
    #     time_counter += timetaken

    #     stop_time = d_setting.DT - (time_counter % d_setting.DT)
    #     stop_gain = calculate_energy(time_counter, time_counter + stop_time)
    #     time_counter += stop_time

    #     # day_counter += 1
    #     pass
present_battery_cent = None

for i in range(5):
    #d_setting.set_day_state(day_counter, i, time_counter)
    if i == 0:
        present_battery_cent = 100
        stop_gain = 0
        cum_d = 0
    else:
        # stop_gain = (200 / 3600) * d_config.PANEL_AREA * d_config.PANEL_EFFICIENCY * (np.sum(calc_solar_irradiance(np.array(range(6 * 3600, 8 * 3600, 200)))) + np.sum(calc_solar_irradiance(np.array(range(17 * 3600, 18 * 3600, 200)))))
        stop_gain = calculate_energy(6 * 3600, 8 * 3600) + calculate_energy(17 * 3600, 18 * 3600)
        present_battery_cent = np.array(outdf['Battery'])[-1]
        cum_d = np.array(outdf['Cumulative Distance'])[-1]
        present_battery_cent = min(present_battery_cent + (stop_gain / d_config.BATTERY_CAPACITY) * 100, 100)

    d_setting.set_day(day_counter, present_battery_cent, i, time_counter)

    outdf, timetaken = main(d_setting.route_df, cum_d, i)
    outdf['Time'] = outdf['Time'] + T * i
    outdf['Cumulative Distance'] += cum_d 
    df_list.append(outdf)
    time_counter += timetaken
    day_counter += 1

dfnet = pd.concat(df_list)
dfnet.to_csv('run_dat.csv', index=False)
print("Written 5days data to `run_dat.csv`")