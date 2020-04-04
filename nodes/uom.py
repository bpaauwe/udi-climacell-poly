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
            'GV9': 56,      # moon phase
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
            'GV9': 56,      # moon phase
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
            'GV9': 56,      # moon phase
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
