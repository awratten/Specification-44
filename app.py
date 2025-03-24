

"""
Cooling load
The calculated amount of energy removed from the cooled spaces of the
building annually by artificial means to maintain the desired 
temperatures in those spaces.
"""

"""
Heating degree hours
For any one hour when the mean outdoor air temperature is less than 15°C,
the degrees Celsius temperature difference between the mean outdoor air
temperature and 15°C
"""

"""
Cooling degree hours
For any one hour when the mean outdoor air temperature is above the
assumed cooling thermostat set point, the degree Celsius air temperature
difference between the mean outdoor air temperature and the assumed 
coolingthermostat set point.
"""

"""
Dehumidification gram hours
For any one hour when the mean humidity is more than 15.7g/kg, the grams
per kilogram of absolute humidity difference between the mean outdoor
absolute humidity and 15.7g/kg.
"""


"""
Habitable room
A room used for normal domestic activities, and—

includes a bedroom, living room, lounge room, music room, television room,
kitchen, dining room, sewing room, study, playroom, family room, home theatre
and sunroom; but

excludes a bathroom, laundry, water closet, pantry, walk-in wardrobe,
corridor, hallway, lobby, photographic darkroom, clothes-drying room,
and other spaces of a specialised nature occupied neither frequently
nor for extended periods.
"""


import parse_nathers_weather_file as weather_parser

def calculate_heating_load_limit(area, hdh):
    """
    Calculate the heating load limit (HLL) for a building.
    :param area: Total habitable room area in square meters.
    :param hdh: Heating Degree Hours.
    :return: Heating Load Limit (HLL).
    """
    fh = calculate_area_adjustment_factor_heating(area)
    return max(4, ((0.0044 * hdh) - 5.9) * fh)

def calculate_area_adjustment_factor_heating(area):
    """
    Calculate adjustment factor based on the size of habitable room area for heating calculations.
    """
    if area <= 50:
        return 1.37
    elif area <= 350:
        return (5.11e-6) * (area ** 2) - (3.82e-3) * area + 1.55
    return 0.84

def calculate_cooling_load_limit(area, cdh, dgh):
    """
    Calculate the cooling load limit (CLL) for a building.
    :param area: Total habitable room area in square meters.
    :param cdh: Cooling Degree Hours.
    :param dgh: Dehumidification Gram Hours.
    :return: Cooling Load Limit (CLL).
    """
    fc = calculate_area_adjustment_factor_cooling(area)
    return (5.4 + 0.00617 * (cdh + 1.85 * dgh)) * fc

def calculate_area_adjustment_factor_cooling(area):
    """
    Calculate adjustment factor based on the size of habitable room area for cooling calculations.
    """
    if area <= 50:
        return 1.34
    elif area <= 200:
        return (1.29e-5) * (area ** 2) - (5.55e-3) * area + 1.58
    elif area <= 1000:
        return (3.76e-7) * (area ** 2) - (7.82e-4) * area + 1.12
    return 0.71

def calculate_total_load_limit(hll, cll, tr):
    """
    TLL = the thermal energy load limit
    HLL = the heating load limit
    CLL = the cooling load limit
    Tr = the annual average daily outdoor temperature range.
    """
    return (19.3 * hll + 22.6 * cll - 8.4) / (tr + 10.74) - 15


# TEST DATA - Melbourne RO
filename = "climat21.TXT" # Melbourne RO
results = weather_parser.analyze_weather_file(filename)

print("Melbourne RO")

print(f"Heating Degree Hours: {results['HDH']:.2f}")
print(f"Cooling Degree Hours: {results['CDH']:.2f}")
print(f"Dehumidification Gram Hours: {results['DGH']:.2f} g/kg·h")
print(f"Average Daily Temperature Range: {results['Avg_Daily_Temp_Range']:.2f}")

HDH = results['HDH']
CDH = results['CDH']
DGH = results['DGH']
Tr = results['Avg_Daily_Temp_Range']

Area = 150 # Total area of the habitable rooms (AH)

HLL = calculate_heating_load_limit(Area, HDH)
CLL = calculate_cooling_load_limit(Area, CDH, DGH)
TLL = calculate_total_load_limit(HLL, CLL, Tr)

print("Heating",HLL)
print("Cooling", CLL)
print("Total" , TLL)


# NatHERS - Melbourne RO
# Heating 48
# Cooling 41
# Total 62

# Specification 44 - Melbourne RO
# Heating 63.19412201500002
# Cooling 21.11161000328479
# Total 73.56015052622135