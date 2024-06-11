'''
Solar power calculation
'''
import numpy as np

from d_config import PANEL_AREA, PANEL_EFFICIENCY
from d_setting import RaceStartTime, DT

def calc_solar_irradiance(time):
    '''
    Find Solar irradiance assuming Gausian distribution each day (temporary until solar data)
    '''
    return 1073.099 * np.exp(-0.5 * ((time - 43200) / 11600) ** 2)

def calculate_incident_solarpower(globaltime, latitude, longitude):
    '''
    Find instantanious solar power generated
    '''
    gt = globaltime % DT # gives time spent on current day
    lt = RaceStartTime + gt # local time on current day
    intensity = calc_solar_irradiance(lt)
    return PANEL_AREA * PANEL_EFFICIENCY * intensity