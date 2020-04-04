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
#from nodes import weather_codes as wx
import node_funcs

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class DailyNode(polyinterface.Node):
    id = 'daily'
    # TODO: add wind speed min/max, pop, winddir min/max
    drivers = [
            {'driver': 'GV19', 'value': 0, 'uom': 25},     # day of week
            {'driver': 'GV0', 'value': 0, 'uom': 4},       # high temp
            {'driver': 'GV1', 'value': 0, 'uom': 4},       # low temp
            {'driver': 'CLIHUM', 'value': 0, 'uom': 22},   # humidity
            {'driver': 'BARPRES', 'value': 0, 'uom': 117}, # pressure
            {'driver': 'GV11', 'value': 0, 'uom': 25},     # coverage
            {'driver': 'GV12', 'value': 0, 'uom': 25},     # intensity
            {'driver': 'GV13', 'value': 0, 'uom': 25},     # weather
            {'driver': 'GV14', 'value': 0, 'uom': 22},     # clouds
            {'driver': 'SPEED', 'value': 0, 'uom': 49},    # wind speed
            {'driver': 'GV5', 'value': 0, 'uom': 49},      # gust speed
            {'driver': 'GV6', 'value': 0, 'uom': 82},      # precipitation
            {'driver': 'GV15', 'value': 0, 'uom': 82},     # snow depth
            {'driver': 'GV7', 'value': 0, 'uom': 49},      # wind speed max
            {'driver': 'GV8', 'value': 0, 'uom': 49},      # wind speed min
            {'driver': 'GV18', 'value': 0, 'uom': 22},     # pop
            {'driver': 'UV', 'value': 0, 'uom': 71},       # UV index
            {'driver': 'GV20', 'value': 0, 'uom': 106},    # mm/day
            ]
    uom = {'GV19': 25,
            'GV0': 4,
            'GV1': 4,
            'CLIHUM': 22,
            'BARPRES': 117,
            'GV11': 25,
            'GV12': 25,
            'GV13': 25,
            'GV14': 22,
            'GV15': 82,
            'SPEED': 49,
            'GV5': 49,
            'GV6': 82,
            'GV7': 49,
            'GV8': 49,
            'UV': 71,
            'GV20': 106,
            'GV18': 22,
            }

    def set_driver_uom(self, units):
        self.uom = uom.get_uom(units)
        self.units = units

    def mm2inch(self, mm):
        return mm/25.4


    def update_forecast(self, forecast, latitude, elevation, plant_type, tags, force):

        epoch = int(forecast['timestamp'])
        dow = time.strftime("%w", time.gmtime(epoch))
        LOGGER.info('Day of week = ' + dow)
        LOGGER.info(tags)

        humidity = (forecast[tags['humidity_min']] + forecast[tags['humidity_max']]) / 2
        try:
            self.update_driver('CLIHUM', humidity, force, prec=0)
            self.update_driver('BARPRES', forecast[tags['pressure']], force, prec=1)
            self.update_driver('GV0', forecast[tags['temp_max']], force, prec=1)
            self.update_driver('GV1', forecast[tags['temp_min']], force, prec=1)
            self.update_driver('GV14', forecast['sky'], force, prec=0)
            self.update_driver('SPEED', forecast[tags['windspeed']], force, prec=1)
            self.update_driver('GV5', forecast[tags['gustspeed']], force, prec=1)
            self.update_driver('GV6', forecast[tags['precipitation']], force, prec=1)
            self.update_driver('GV7', forecast[tags['wind_max']], force, prec=1)
            self.update_driver('GV8', forecast[tags['wind_min']], force, prec=1)
            self.update_driver('GV15', (float(forecast[tags['snowf']]) * 10), force, prec=2)
            self.update_driver('GV19', int(dow), force)
            self.update_driver('UV', forecast['uvi'], force, prec=1)
            self.update_driver('GV18', forecast['pop'], force, prec=1)

            LOGGER.debug('Forecast coded weather = ' + forecast['weatherPrimaryCoded'])
            weather = forecast['weatherPrimaryCoded'].split(':')[0]
            self.update_driver('GV11', wx.coverage_codes(weather), force)
            weather = forecast['weatherPrimaryCoded'].split(':')[1]
            self.update_driver('GV12', wx.intensity_codes(weather), force)
            weather = forecast['weatherPrimaryCoded'].split(':')[2]
            self.update_driver('GV13', wx.weather_codes(weather), force)

        except Exception as e:
            LOGGER.error('Forcast: ' + str(e))

        # Calculate ETo
        #  Temp is in degree C and windspeed is in m/s, we may need to
        #  convert these.
        J = datetime.datetime.fromtimestamp(epoch).timetuple().tm_yday

        Tmin = forecast[tags['temp_min']]
        Tmax = forecast[tags['temp_max']]
        Ws = forecast[tags['windspeed']]
        if self.units != 'si':
            LOGGER.info('Conversion of temperature/wind speed required')
            Tmin = et3.FtoC(Tmin)
            Tmax = et3.FtoC(Tmax)
            Ws = et3.mph2ms(Ws)
        else:
            Ws = et3.kph2ms(Ws)

        et0 = et3.evapotranspriation(Tmax, Tmin, None, Ws, float(elevation), forecast[tags['humidity_max']], forecast[tags['humidity_min']], latitude, float(plant_type), J)
        if self.units == 'metric' or self.units == 'si' or self.units.startswith('m'):
            self.update_driver('GV20', round(et0, 2), force)
        else:
            self.update_driver('GV20', self.mm2inch(et0), force, prec=3)
        LOGGER.info("ETo = %f %f" % (et0, self.mm2inch(et0)))
