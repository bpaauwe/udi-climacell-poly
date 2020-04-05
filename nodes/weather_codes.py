def weather_code(code_str):
    if code_str == 'freezing_rain_heavy':
        return 1
    elif code_str == 'freezing_rain':
        return 2
    elif code_str == 'freezing_rain_light':
        return 3
    elif code_str == 'freezing_drizzle':
        return 4
    elif code_str == 'ice_pellets_heavy':
        return 5
    elif code_str == 'ice_pellets':
        return 6
    elif code_str == 'ice_pellets_light':
        return 7
    elif code_str == 'snow_heavy':
        return 8
    elif code_str == 'snow':
        return 9
    elif code_str == 'snow_light':
        return 10
    elif code_str == 'flurries':
        return 11
    elif code_str == 'tstorm':
        return 12
    elif code_str == 'rain_heavy':
        return 13
    elif code_str == 'rain':
        return 14
    elif code_str == 'rain_light':
        return 15
    elif code_str == 'drizzle':
        return 16
    elif code_str == 'fog_light':
        return 17
    elif code_str == 'fog':
        return 18
    elif code_str == 'cloudy':
        return 19
    elif code_str == 'mostly_cloudy':
        return 20
    elif code_str == 'partly_cloudy':
        return 21
    elif code_str == 'mostly_clear':
        return 22
    elif code_str == 'clear':
        return 23

    return 0

def moon_phase(moon_str):
    if moon_str == 'new_moon':
        return 0.0
    elif moon_str == 'waxing_crescent':
        return .25
    elif moon_str == 'first_quarter':
        return .5
    elif moon_str == 'waxing_gibbous':
        return .75
    elif moon_str == 'full_moon':
        return 1.0
    elif moon_str == 'waning_gibbous':
        return .75
    elif moon_str == 'third_quarter':
        return .5
    elif moon_str == 'waning_crescent':
        return .25

    return 0.0
