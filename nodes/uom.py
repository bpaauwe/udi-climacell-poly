#
#  Unit of Measure configuration function
#
#  Return a dictionary with driver names as the key and the UOM for
#  the requested unit configuration.
#
#  valid unit configurations are:
#   metric, imperial, si (same as metric), us (same as imperial), uk
#
#  Ideally, there should be no conflicts between forecast and current
#  condition driver types


def get_uom(units):
    unit_cfg = units.lower()

    if unit_cfg == 'metric' or unit_cfg == 'si' or unit_cfg.startswith('m'):
        uom = {
            'ST': 2,   # node server status
            'CLITEMP': 4,   # temperature
            'CLIHUM': 22,   # humidity
            'BARPRES': 117, # pressure
            'WINDDIR': 76,  # direction
            'DEWPT': 4,     # dew point
            'SOLRAD': 74,   # solar radiation
            'RAINRT': 46,   # rain rate
            'GV0': 4,       # max temp
            'GV1': 4,       # min temp
            'GV2': 4,       # ??feels like
            'GV3': 4,       # heat index  
            'GV4': 4,       # wind chill
            'SPEED': 49,    # wind speed
            'GV5': 49,      # wind gusts
            'GV6': 82,      # rain
            'GV7': 49,      # wind max
            'GV8': 49,      # wind min  
            'GV9': 25,      # moon phase
            'GV10': 56,     # ozone
            'GV11': 25,     # climate coverage
            'GV12': 25,     # climate intensity
            'GV13': 25,     # climate conditions
            'GV14': 22,     # cloud conditions
            'GV15': 82,     # snow depth
            'DISTANC': 83,  # visibility (kilometers)
            'UV': 71,       # UV index
            'GV17': 56,     # Air Quality
            'GV18': 22,     # chance of precipitation
            'GV19': 25,     # day of week
            'GV20': 106,    # ETo
        }
    elif unit_cfg == 'uk':
        uom = {
            'ST': 2,   # node server status
            'CLITEMP': 4,   # temperature
            'CLIHUM': 22,   # humidity
            'BARPRES': 117, # pressure
            'WINDDIR': 76,  # direction
            'DEWPT': 4,     # dew point
            'SOLRAD': 74,   # solar radiation
            'RAINRT': 24,   # rain rate
            'GV0': 4,       # max temp
            'GV1': 4,       # min temp
            'GV2': 4,       # feels like
            'GV3': 4,       # ??feels like
            'GV4': 4,       # wind chill
            'SPEED': 48,    # wind speed
            'GV5': 48,      # wind gusts
            'GV6': 105,     # rain
            'GV7': 48,      # max wind
            'GV8': 48,      # min wind  
            'GV9': 25,      # moon phase
            'GV10': 56,     # ozone
            'GV11': 25,     # climate coverage
            'GV12': 25,     # climate intensity
            'GV13': 25,     # climate conditions
            'GV14': 22,     # cloud conditions
            'GV15': 105,    # snow depth
            'DISTANC': 116, # visibility
            'UV': 71,       # UV index
            'GV17': 56,     # Air Quality
            'GV18': 22,     # chance of precipitation
            'GV19': 25,     # day of week
            'GV20': 120,    # ETo
        }
    else:
        uom = {
            'ST': 2,   # node server status
            'CLITEMP': 17,  # temperature
            'CLIHUM': 22,   # humidity
            'BARPRES': 23,  # pressure
            'WINDDIR': 76,  # direction
            'DEWPT': 17,    # dew point
            'SOLRAD': 74,   # solar radiation
            'RAINRT': 24,   # rain rate
            'GV0': 17,      # max temp
            'GV1': 17,      # min temp
            'GV2': 17,      # feels like
            'GV3': 17,      # ??feels like
            'GV4': 17,      # wind chill
            'SPEED': 48,    # wind speed
            'GV5': 48,      # wind gusts
            'GV6': 105,     # rain
            'GV7': 48,      # max wind
            'GV8': 48,      # min wind   
            'GV9': 25,      # moon phase
            'GV10': 56,     # ozone
            'GV11': 25,     # climate coverage
            'GV12': 25,     # climate intensity
            'GV13': 25,     # climate conditions
            'GV14': 22,     # cloud conditions
            'GV15': 105,    # snow depth
            'DISTANC': 116, # visibility
            'UV': 71,       # UV index
            'GV17': 56,     # Air Quality
            'GV18': 22,     # chance of precipitation
            'GV19': 25,     # day of week
            'GV20': 120,    # ETo
        }

    return uom

"""
For conversions, u will be either uk or something else to indicate us. For
some cases, there is no conversion for UK
"""
def c2f(temp, u):
    if u == 'uk':
        return temp

    return round((temp * 9 / 5) + 32, 1)

def hpa2hgin(pressure, u):
    if u == 'uk':
        return pressure

    return round(pressure * 0.02953, 3)

def mmh2inh(rain, u):
    return round(rain * 0.393701, 3)

def ms2mph(speed, u):
    return round(speed * 2.23694, 1)

def mm2in(rain, u):
    return round(rain * 0.393701, 3)

def km2mile(distance, u):
    return round(distance * .621371, 1)

# convert the value based on the driver.  Incoming units are
# assumed to be metric.
def conversion(driver, units, value):
    unit_cfg = units.lower()

    function_map = {
            'ST': None,   # node server status
            'CLITEMP': c2f,   # temperature
            'CLIHUM': None,   # humidity
            'BARPRES': hpa2hgin, # pressure
            'WINDDIR': None,  # direction
            'DEWPT': c2f,     # dew point
            'SOLRAD': None,   # solar radiation
            'RAINRT': mmh2inh,   # rain rate
            'GV0': c2f,       # max temp
            'GV1': c2f,       # min temp
            'GV2': c2f,       # ??feels like
            'GV3': c2f,       # heat index  
            'GV4': c2f,       # wind chill
            'SPEED': ms2mph,    # wind speed
            'GV5': ms2mph,      # wind gusts
            'GV6': mm2in,      # rain
            'GV7': ms2mph,      # wind max
            'GV8': ms2mph,      # wind min  
            'GV9': None,      # moon phase
            'GV10': None,     # ozone
            'GV11': None,     # climate coverage
            'GV12': None,     # climate intensity
            'GV13': None,     # climate conditions
            'GV14': None,     # cloud conditions
            'GV15': mm2in,     # snow depth
            'DISTANC': km2mile,  # visibility (kilometers)
            'UV': None,       # UV index
            'GV17': None,     # Air Quality
            'GV18': None,     # chance of precipitation
            'GV19': None,     # day of week
            'GV20': mm2in,    # ETo
    }

    if driver not in function_map:
        return value

    if function_map[driver] == None:
        return value

    if unit_cfg == 'metric' or unit_cfg == 'si' or unit_cfg.startswith('m'):
        return value

    return function_map[driver](value, unit_cfg)
