# Node definition for a daily forecast node

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface

import json
import time
import datetime
from nodes import et3
from nodes import uom
from nodes import weather_codes as wx
import node_funcs

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class DailyNode(polyinterface.Node):
    id = 'daily'
    drivers = [
            {'driver': 'GV19', 'value': 0, 'uom': 25},     # day of week
            {'driver': 'GV0', 'value': 0, 'uom': 4},       # high temp
            {'driver': 'GV1', 'value': 0, 'uom': 4},       # low temp
            {'driver': 'CLIHUM', 'value': 0, 'uom': 22},   # humidity
            {'driver': 'BARPRES', 'value': 0, 'uom': 117}, # pressure
            {'driver': 'GV13', 'value': 0, 'uom': 25},     # weather
            {'driver': 'GV6', 'value': 0, 'uom': 82},      # precipitation
            {'driver': 'RAINRT', 'value': 0, 'uom': 46},   # precipitation rate
            {'driver': 'GV7', 'value': 0, 'uom': 49},      # wind speed max
            {'driver': 'GV8', 'value': 0, 'uom': 49},      # wind speed min
            {'driver': 'GV18', 'value': 0, 'uom': 22},     # pop
            {'driver': 'GV20', 'value': 0, 'uom': 106},    # mm/day
            ]

    def set_driver_uom(self, units):
        self.uom = uom.get_uom(units)
        self.units = units

    def mm2inch(self, mm):
        return mm/25.4


    def get_min_max(self, key, data):
        min_val = 0
        max_val = 0
        if key in data:
            for r in data[key]:
                if 'max' in r:
                    max_val = r['max']['value']
                if 'min' in r:
                    min_val = r['min']['value']

        return (min_val, max_val)

    def update_forecast(self, forecast, latitude, elevation, plant_type, force):

        try:
            (year, month, day) = forecast['observation_time']['value'].split('-')
            forecast_day = datetime.datetime(int(year), int(month), int(day))
            dow = forecast_day.weekday()
        except Exception as e:
            LOGGER.error('get day of week: ' + str(e))
            dow = 0

        (hmin, hmax) = self.get_min_max('humidity', forecast)
        LOGGER.debug('humidity = ' + str(hmin) + ' / ' + str(hmax))
        humidity = (hmin + hmax) / 2
        #humidity = (forecast['humidity'][0]['min']['value'] + forecast['humidity'][1]['max']['value']) / 2

        try:
            (tmin, tmax) = self.get_min_max('temp', forecast)
            self.update_driver('GV0', tmax, force, prec=1)
            self.update_driver('GV1', tmin, force, prec=1)
            self.update_driver('CLIHUM', humidity, force, prec=0)

            # TODO: min/max pressure
            (vmin, vmax) = self.get_min_max('baro_pressure', forecast)
            self.update_driver('BARPRES', vmax, force, prec=1)
            # rate: self.update_driver('GV6', forecast['preciptiation'][0]['max']['value'], force, prec=1)

            self.update_driver('GV6', forecast['precipitation_accumulation']['value'], force, prec=1)
            self.update_driver('RAINRT', forecast['precipitation'][0]['max']['value'], force, prec=3)

            (vmin, vmax) = self.get_min_max('wind_speed', forecast)
            Ws = (vmin + vmax) / 2
            self.update_driver('GV7', vmax, force, prec=1)
            self.update_driver('GV8', vmin, force, prec=1)
            self.update_driver('GV19', int(dow), force)
            self.update_driver('GV18', forecast['precipitation_probability']['value'], force, prec=1)

            #TODO: add visibility(min/max), moon phase, feelslike(min/max)

            LOGGER.debug('Forecast coded weather = ' + forecast['weather_code']['value'])
            self.update_driver('GV13', wx.weather_code(forecast['weather_code']['value']), force)

        except Exception as e:
            LOGGER.error('Forcast: ' + str(e))

        # Calculate ETo
        #  Temp is in degree C and windspeed is in m/s, we may need to
        #  convert these.
        #J = datetime.datetime.fromtimestamp(epoch).timetuple().tm_yday
        J = forecast_day.timetuple().tm_yday

        try:
            if self.units != 'si':
                LOGGER.info('Conversion of temperature/wind speed required')
                tmin = et3.FtoC(tmin)
                tmax = et3.FtoC(tmax)
                Ws = et3.mph2ms(Ws)
            else:
                Ws = et3.kph2ms(Ws)
        except Exception as e:
            LoGGER.error('conversion issue: ' + str(e))

        et0 = et3.evapotranspriation(tmax, tmin, None, Ws, float(elevation), hmax, hmin, float(latitude), float(plant_type), J)
        if self.units == 'metric' or self.units == 'si' or self.units.startswith('m'):
            self.update_driver('GV20', round(et0, 2), force)
        else:
            self.update_driver('GV20', self.mm2inch(et0), force, prec=3)
        LOGGER.info("ETo = %f %f" % (et0, self.mm2inch(et0)))
