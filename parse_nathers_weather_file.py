"""
Characters Item
 1 - 2 location identification (e.g.ME represents Melbourne)
 3 - 4 year (e.g. 67)
 5 - 6 month (i.e. 1 - 12)
 7 - 8 day (i.e. 1 - 31)
 9 - 10 hour standard (i.e. 0-23, 0 = midnight)
 11 - 14 dry bulb temperature (10-1 °C)
 15 - 17 absolute moisture content (10-1 g/kg)
 18 - 21 atmospheric pressure (10-1 kPa)
 22 - 24 wind speed (10-1 m/s)
 25 - 26 wind direction (0-16; 0 = CALM. 1 = NNE ,...,16 = N)

 27 total cloud cover (oktas, 0 - 8)
 28 flag relating to dry bulb temperature
 29 flag relating to absolute moisture content
 30 flag relating to atmospheric pressure
 31 flag relating to wind speed and direction
 32 flag relating to total cloud cover
 33 blank

 34 - 37 global solar irradiance on a horizontal plane (W/m2)
 38 - 40 diffuse solar irradiance on a horizontal plane (W/m2)
 41 - 44 direct solar irradiance on a plane normal to the beam (W/m2)
 45 - 46 solar altitude (degrees, 0-90)
 47 - 49 solar azimuth (degrees, 0-360)
 50 flag relating to global and diffuse solar irradiance
 51 flag }
 52 - 56 Australian Met Station Number } Some locations only
 57 - 61 wet bulb temperature (10-1 °C) }
 62 - 81 Station name (first line only) }

 Values for flags relating to standard surface meteorological data (columns 28 - 32)
 0 means that the value is measured value
 1 means that the value is estimated to replace a missing measurement
 2 means that the value is an interpolating between three-hourly measurements
 3 missing value
 Values for flag relating to solar radiation data (column 50)
 0 means that both global and diffuse irradiance values are based on measurements
 1 means that both global and diffuse irradiance values are estimated to
 replace a missing measurement
 2 means that the global irradiance value is based on measurement but the
 diffuse irradiance value is estimated to replace a missing measurement
 3 missing value or estimated value from cloud cover data
 4 interpolated value from three hourly data
"""


from dataclasses import dataclass
from collections import defaultdict

@dataclass
class WeatherData:
    LocationID: str
    year: int
    month: int
    day: int
    hour_standard: int
    dry_bulb_temperature: float  # Degrees C
    absolute_moisture_content: float  # g/kg
    atmospheric_pressure: int  # hPa
    wind_speed: float  # m/s
    wind_direction: int
    wind_direction_string: str
    total_cloud_cover_oktas: int
    flag_dry_bulb_temperature: int
    flag_absolute_moisture_content: int
    flag_atmospheric_pressure: int
    flag_wind_speed_direction: int
    flag_total_cloud_cover: int
    global_solar_radiation_horizontal: int
    diffuse_solar_radiaton_horizontal: int
    direct_solar_radiation_normal_plane: int
    solar_altitude: int
    solar_azimuth: int
    flag_global_diffuse_solar_irradiance: int
    flag_unknown: int
    met_station_number: int
    wet_bulb_temperature: float


def read_col(string, start_col, end_col):
    """Extracts a substring from a fixed-width formatted string."""
    x = string[start_col - 1:end_col].strip()
    return x if x else None


def safe_int(value, default=0):
    """Converts a value to int, returns default if conversion fails."""
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


def safe_float(value, scale=1, default=0.0):
    """Converts a value to float, applies scale, and returns default if conversion fails."""
    try:
        return float(value) / scale if value is not None else default
    except ValueError:
        return default


def parse_wind_direction(value):
    wind_directions = {
        0: "Calm", 1: "NNE", 2: "NE", 3: "ENE", 4: "E",
        5: "ESE", 6: "SE", 7: "SSE", 8: "S", 9: "SSW",
        10: "SW", 11: "WSW", 12: "W", 13: "WNW", 14: "NW",
        15: "NNW", 16: "N"
    }
    return wind_directions.get(value, "Unknown")


def parse_weather_file(filename):
    parsed_data = []
    
    with open(filename, 'r') as file:
        for line in file:
            wd = WeatherData(
                LocationID=read_col(line, 1, 2),
                year=safe_int(read_col(line, 3, 4)),
                month=safe_int(read_col(line, 5, 6)),
                day=safe_int(read_col(line, 7, 8)),
                hour_standard=safe_int(read_col(line, 9, 10)),
                dry_bulb_temperature=safe_float(read_col(line, 11, 14), 10),
                absolute_moisture_content=safe_float(read_col(line, 15, 17), 10),
                atmospheric_pressure=safe_int(read_col(line, 18, 21)),
                wind_speed=safe_float(read_col(line, 22, 24), 10),
                wind_direction=safe_int(read_col(line, 25, 26)),
                wind_direction_string=parse_wind_direction(safe_int(read_col(line, 25, 26))),
                total_cloud_cover_oktas=safe_int(read_col(line, 27, 27)),
                flag_dry_bulb_temperature=safe_int(read_col(line, 28, 28)),
                flag_absolute_moisture_content=safe_int(read_col(line, 29, 29)),
                flag_atmospheric_pressure=safe_int(read_col(line, 30, 30)),
                flag_wind_speed_direction=safe_int(read_col(line, 31, 31)),
                flag_total_cloud_cover=safe_int(read_col(line, 32, 32)),
                global_solar_radiation_horizontal=safe_int(read_col(line, 34, 37)),
                diffuse_solar_radiaton_horizontal=safe_int(read_col(line, 38, 40)),
                direct_solar_radiation_normal_plane=safe_int(read_col(line, 41, 44)),
                solar_altitude=safe_int(read_col(line, 45, 46)),
                solar_azimuth=safe_int(read_col(line, 47, 49)),
                flag_global_diffuse_solar_irradiance=safe_int(read_col(line, 50, 50)),
                flag_unknown=safe_int(read_col(line, 51, 51)),
                met_station_number=safe_int(read_col(line, 52, 56)),
                wet_bulb_temperature=safe_float(read_col(line, 57, 61), 10)
            )

            parsed_data.append(wd)

    return parsed_data


def calculate_heating_degree_hours(weather_data, base_temp=15):
    return sum((base_temp - data.dry_bulb_temperature) for data in weather_data if data.dry_bulb_temperature < base_temp)


def calculate_cooling_degree_hours(weather_data):
    """Get the neutral temperature (desired by occupants) according to ASHRAE-55.

    Note:
        [1] de Dear, R.J. and Brager, G.S. (2002) Thermal comfort in naturally
        ventilated buildings: Revisions to ASHRAE Standard 55.
        Energy and Buildings 34(6), 549-61.

        [2] de Dear, R.J. (1998) A global database of thermal comfort experiments.
        ASHRAE Technical data bulletin 14(1), 15-26.

    Args:
        Tm: The prevailing outdoor temperature [C].  For the ASHRAE-55 adaptive
            comfort model, this is typically the average monthly outdoor temperature.

    Return:
        The desired neutral temperature for the input prevailing outdoor temperature.
    """

 
    # Calculate mean January outdoor air temperature
    january_temps = [data.dry_bulb_temperature for data in weather_data if data.month == 1]
    Tm = sum(january_temps) / len(january_temps) if january_temps else 0  # Avoid division by zero
    
    # Compute thermally neutral seems to be taken from ASHRE 55 adaptive thermal comfort model
    summer_thermally_neutral = 17.8 + 0.31 * Tm
    
    # Set limits based on HSTAR documentation
    if summer_thermally_neutral > 28.5:
        summer_thermally_neutral = 28.5
    elif summer_thermally_neutral < 22.5:
        summer_thermally_neutral = 22.5
    
    # Round set point to 0.1
    summer_thermally_neutral = round(summer_thermally_neutral, 1)
    
    return sum((data.dry_bulb_temperature - summer_thermally_neutral) for data in weather_data if data.dry_bulb_temperature > summer_thermally_neutral), summer_thermally_neutral





def calculate_dehumidification_gram_hours(weather_data, humidity_threshold=15.7):
    return sum((data.absolute_moisture_content - humidity_threshold) for data in weather_data if data.absolute_moisture_content > humidity_threshold)


def calculate_avg_daily_temp_range(weather_data):
    daily_temps = defaultdict(lambda: {"max": float("-inf"), "min": float("inf")})

    for data in weather_data:
        key = (data.month, data.day)
        daily_temps[key]["max"] = max(daily_temps[key]["max"], data.dry_bulb_temperature)
        daily_temps[key]["min"] = min(daily_temps[key]["min"], data.dry_bulb_temperature)

    daily_temp_ranges = [(temps["max"] - temps["min"]) for temps in daily_temps.values()]
    return sum(daily_temp_ranges) / len(daily_temp_ranges) if daily_temp_ranges else 0


def analyze_weather_file(filename):
    parsed_result = parse_weather_file(filename)

    return {
        "HDH": calculate_heating_degree_hours(parsed_result),
        "CDH": calculate_cooling_degree_hours(parsed_result),
        "DGH": calculate_dehumidification_gram_hours(parsed_result),
        "Avg_Daily_Temp_Range": calculate_avg_daily_temp_range(parsed_result),
    }


if __name__ == "__main__":
    filename = "climat67.TXT"
    results = analyze_weather_file(filename)

    print(f"Total Heating Degree Hours: {results['HDH']:.2f}")
    print(f"Total Cooling Degree Hours: {results['CDH']:.2f}")
    print(f"Total Dehumidification Gram Hours: {results['DGH']:.2f} g/kg·h")
    print(f"Average Daily Temperature Range: {results['Avg_Daily_Temp_Range']:.2f}")
