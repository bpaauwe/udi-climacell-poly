#!/usr/bin/env python3
"""
Polyglot v2 node server climacell weather data
Copyright (C) 2020 Robert Paauwe
"""

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import datetime
import requests
import socket
import math
import re
import json
import node_funcs
from datetime import timedelta
from nodes import climacell_daily
from nodes import uom
from nodes import weather_codes as wx

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class Controller(polyinterface.Controller):
    id = 'weather'
    #id = 'controller'
    hint = [0,0,0,0]
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'Climacell Weather'
        self.address = 'weather'
        self.primary = self.address
        self.configured = False
        self.latitude = 0
        self.longitude = 0
        self.force = True

        self.params = node_funcs.NSParameters([{
            'name': 'APIKey',
            'default': 'set me',
            'isRequired': True,
            'notice': 'climacell API key must be set',
            },
            {
            'name': 'Latitude',
            'default': '-59.9 to 59.9',
            'isRequired': True,
            'notice': 'Latitude must be set',
            },
            {
            'name': 'Longitude',
            'default': '-180 to 180',
            'isRequired': True,
            'notice': 'Longitude must be set',
            },
            {
             'name': 'Units',
            'default': 'us',
            'isRequired': False,
            'notice': '',
            },
            {
            'name': 'Forecast Days',
            'default': '0',
            'isRequired': False,
            'notice': '',
            },
            {
            'name': 'Elevation',
            'default': '0',
            'isRequired': False,
            'notice': '',
            },
            {
            'name': 'Plant Type',
            'default': '0.23',
            'isRequired': False,
            'notice': '',
            },
            ])


        self.poly.onConfig(self.process_config)

    # Process changes to customParameters
    def process_config(self, config):
        (valid, changed) = self.params.update_from_polyglot(config)
        if changed and not valid:
            LOGGER.debug('-- configuration not yet valid')
            self.removeNoticesAll()
            self.params.send_notices(self)
        elif changed and valid:
            LOGGER.debug('-- configuration is valid')
            self.removeNoticesAll()
            self.configured = True
            if self.params.isSet('Forecast Days'):
                self.discover()
        elif valid:
            LOGGER.debug('-- configuration not changed, but is valid')

    def start(self):
        LOGGER.info('Starting node server')
        self.check_params()
        self.discover()
        LOGGER.info('Node server started')

        # Do an initial query to get filled in as soon as possible
        self.query_conditions()
        self.query_forecast()
        self.force = False

    def longPoll(self):
        LOGGER.debug('longpoll')
        self.query_forecast()

    def shortPoll(self):
        self.query_conditions()

    def query_conditions(self):
        # Query for the current conditions. We can do this fairly
        # frequently, probably as often as once a minute.

        if not self.configured:
            LOGGER.info('Skipping connection because we aren\'t configured yet.')
            return


        try:
            request = 'https://api.climacell.co/v3/weather/realtime?'
            request += 'lat=' + self.params.get('Latitude')
            request += '&lon=' + self.params.get('Longitude')
            request += '&unit_system=' + self.params.get('Units')
            request += '&fields=precipitation,precipitation_type,temp,feels_like,dewpoint,wind_speed,wind_gust,baro_pressure,visibility,humidity,wind_direction,fire_index,sunrise,sunset,cloud_cover,cloud_ceiling,cloud_base,surface_shortwave_radiation,moon_phase,weather_code,epa_aqi,epa_primary_pollutant,pm25,pm10,o3,no2,co,so2,epa_health_concern'

            # currently only supports metric units!
            request = 'https://data.climacell.co/v4/timelines?'
            request += 'location=' + self.params.get('Latitude') + ','
            request += self.params.get('Longitude')
            request += '&timesteps=5m'
            request += '&fields=precipitationIntensity,precipitationType,temperature,temperatureApparent,dewPoint,windSpeed,windGust,pressureSeaLevel,visibility,humidity,windDirection,cloudCover,cloudCeiling,cloudBase,solarGHI,weatherCode,epaIndex'

            # sunrise/sunsetTime and moon phase require 1 day stimesteps

            headers = {
                    'apikey': self.params.get('APIKey'), 
                    'Content-Type': 'application/JSON'
                    }

            c = requests.get(request, headers=headers)
            jdata = c.json()
            c.close()

            # data should be under 'data' / 'timelines' / [0] / 'intervals / [0]

            interval = jdata['data']['timelines'][0]['intervals'][0]
            LOGGER.debug('REALTIME: {}'.format(interval))

            if jdata == None:
                LOGGER.error('Current condition query returned no data')
                return

            values = interval['values']
        
            """
            All values are metric so we will have to do the conversions
            before sending the data to the ISY if the user want's something
            else.
            """
            u = self.params.get('Units')
            if 'temperature' in values:
                LOGGER.debug('TEMPERATURE: {} {}'.format(u, values['temperature']))
                v = uom.conversion('CLITEMP', u, values['temperature'])
                self.update_driver('CLITEMP', v)
            if 'humidity' in values:
                self.update_driver('CLIHUM', values['humidity'])
            if 'pressureSeaLevel' in values:
                v = uom.conversion('BARPRES', u, values['pressureSeaLevel'])
                self.update_driver('BARPRES', v)
            if 'windSpeed' in values:
                v = uom.conversion('SPEED', u, values['windSpeed'])
                self.update_driver('SPEED', v)
            if 'windGust' in values:
                v = uom.conversion('SPEED', u, values['windGust'])
                self.update_driver('GV5', v)
            if 'windDirection' in values:
                self.update_driver('WINDDIR', values['windDirection'])
            if 'visibility' in values:
                v = uom.conversion('DISTANC', u, values['visibility'])
                self.update_driver('DISTANC', v)
            if 'precipitationIntensity' in values:
                v = uom.conversion('RAINRT', u, values['precipitationIntensity'])
                self.update_driver('RAINRT', v)
            if 'dewPoint' in values:
                v = uom.conversion('DEWPT', u, values['dewPoint'])
                self.update_driver('DEWPT', v)
            if 'temperatureApparent' in values:
                v = uom.conversion('GV2', u, values['temperatureApparent'])
                self.update_driver('GV2', v)
            if 'solarGHI' in values:
                self.update_driver('SOLRAD', values['solarGHI'])
            if 'cloudCover' in values:
                self.update_driver('GV14', values['cloudCover'])
            if 'weatherCode' in values:
                LOGGER.debug('weather code = {}'.format(values['weatherCode']))
                self.update_driver('GV13', values['weatherCode'])
            if 'epaIndex' in values:
                self.update_driver('GV17', values['epaIndex'])


            '''
            TODO:
            - ceiling
            '''
        except Exception as e:
            LOGGER.error('Current observation update failure')
            LOGGER.error(e)

    def query_forecast(self):
        if not self.configured:
            LOGGER.info('Skipping connection because we aren\'t configured yet.')
            return

        try:
            if int(self.params.get('Forecast Days')) > 1:
                enddate = datetime.datetime.utcnow() + timedelta(days=(int(self.params.get('Forecast Days')) - 1))
            else:
                enddate = datetime.datetime.utcnow() + timedelta(days=(int(self.params.get('Forecast Days')))) + timedelta(minutes=1)

            request = 'https://api.climacell.co/v3/weather/forecast/daily?'
            request += 'lat=' + self.params.get('Latitude')
            request += '&lon=' + self.params.get('Longitude')
            request += '&unit_system=' + self.params.get('Units')
            request += '&start_time=now'
            request += '&end_time=' + enddate.strftime('%Y-%m-%dT%H:%M:%SZ')
            request += '&fields=precipitation,precipitation_accumulation,temp,feels_like,wind_speed,baro_pressure,visibility,humidity,wind_direction,precipitation_probability,moon_phase,weather_code'

            request = 'https://data.climacell.co/v4/timelines?'
            request += 'location=' + self.params.get('Latitude') + ','
            request += self.params.get('Longitude')
            request += '&timesteps=1d'
            #request += '&startTime=now'
            request += '&endTime=' + enddate.strftime('%Y-%m-%dT%H:%M:%SZ')
            request += '&fields=precipitationIntensity,precipitationType,precipitationProbability,temperatureMin,temperatureMax,temperatureApparent,dewPoint,windSpeedMin,windSpeedMax,windSpeedAvg,windGust,pressureSeaLevelMin,pressureSeaLevelMax,visibility,humidityMin,humidityMax,humidityAvg,windDirection,cloudCover,cloudCeiling,cloudBase,solarGHI,weatherCode,moonPhase'

            headers = {
                    'apikey': self.params.get('APIKey'), 
                    'Content-Type': 'application/JSON'
                    }

            LOGGER.debug('-------------')
            LOGGER.debug('FORECAST: {}'.format(request))

            c = requests.get(request, headers=headers)
            jdata = c.json()
            c.close()

            LOGGER.debug('FORECAST: {}'.format(jdata))
            intervals = jdata['data']['timelines'][0]['intervals']
            LOGGER.debug('FORECAST: {}'.format(intervals))
            #LOGGER.debug('-------------')

            # Records are for each day, midnight to midnight
            day = 0
            LOGGER.debug('Processing periods: %d' % len(intervals))
            for forecast in intervals:
                address = 'forecast_' + str(day)
                LOGGER.debug(' >>>>   period ' + forecast['startTime'] + '  ' + address)
                LOGGER.debug(forecast)
                self.nodes[address].update_forecast(forecast, self.params.get('Latitude'), self.params.get('Elevation'), self.params.get('Plant Type'), self.force)
                day += 1
                if day >= int(self.params.get('Forecast Days')):
                    return

        except Exception as e:
            LOGGER.error('Forecast data failure: ' + str(e))


    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        # Create any additional nodes here
        LOGGER.info("In Discovery...")

        num_days = int(self.params.get('Forecast Days'))
        if num_days < 15:
            # delete any extra days
            for day in range(num_days, 15):
                address = 'forecast_' + str(day)
                try:
                    self.delNode(address)
                except:
                    LOGGER.debug('Failed to delete node ' + address)

        for day in range(0,num_days):
            address = 'forecast_' + str(day)
            title = 'Forecast ' + str(day)
            try:
                node = climacell_daily.DailyNode(self, self.address, address, title)
                self.addNode(node)
            except Excepton as e:
                LOGGER.error('Failed to create forecast node ' + title)
                LOGGER.error(e)

        self.set_driver_uom(self.params.get('Units'))

    # Delete the node server from Polyglot
    def delete(self):
        LOGGER.info('Removing node server')

    def stop(self):
        LOGGER.info('Stopping node server')

    def update_profile(self, command):
        st = self.poly.installprofile()
        return st

    def check_params(self):
        self.removeNoticesAll()

        if self.params.get_from_polyglot(self):
            LOGGER.debug('All required parameters are set!')
            self.configured = True
            if int(self.params.get('Forecast Days')) > 15:
                addNotice('Number of days of forecast data is limited to 15 days', 'forecast')
                self.params.set('Forecast Days', 15)
        else:
            LOGGER.debug('Configuration required.')
            LOGGER.debug('APIKey = ' + self.params.get('APIKey'))
            LOGGER.debug('Latitude = ' + self.params.get('Latitude'))
            LOGGER.debug('Longitude = ' + self.params.get('Longitude'))
            self.params.send_notices(self)

    # Set the uom dictionary based on current user units preference
    def set_driver_uom(self, units):
        LOGGER.info('Configure driver units to ' + units)
        self.uom = uom.get_uom(units)
        for day in range(0, int(self.params.get('Forecast Days'))):
            address = 'forecast_' + str(day)
            self.nodes[address].set_driver_uom(units)

    def remove_notices_all(self, command):
        self.removeNoticesAll()

    def set_logging_level(self, level=None):
        if level is None:
            try:
                # level = self.getDriver('GVP')
                level = self.get_saved_log_level()
            except:
                LOGGER.error('set_logging_level: get saved log level failed.')

            if level is None:
                level = 30

            level = int(level)
        else:
            level = int(level['value'])

        # self.setDriver('GVP', level, True, True)
        self.save_log_level(level)
        LOGGER.info('set_logging_level: Setting log level to %d' % level)
        LOGGER.setLevel(level)

    commands = {
            'UPDATE_PROFILE': update_profile,
            'REMOVE_NOTICES_ALL': remove_notices_all,
            'DEBUG': set_logging_level,
            }

    # For this node server, all of the info is available in the single
    # controller node.
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},   # node server status
            {'driver': 'CLITEMP', 'value': 0, 'uom': 4},   # temperature
            {'driver': 'CLIHUM', 'value': 0, 'uom': 22},   # humidity
            {'driver': 'DEWPT', 'value': 0, 'uom': 4},     # dewpoint
            {'driver': 'BARPRES', 'value': 0, 'uom': 117}, # pressure
            {'driver': 'WINDDIR', 'value': 0, 'uom': 76},  # direction
            {'driver': 'SPEED', 'value': 0, 'uom': 49},    # wind speed
            {'driver': 'GV5', 'value': 0, 'uom': 49},      # gust speed
            {'driver': 'GV2', 'value': 0, 'uom': 4},       # feels like
            {'driver': 'RAINRT', 'value': 0, 'uom': 46},   # rain
            {'driver': 'GV13', 'value': 0, 'uom': 25},     # climate conditions
            {'driver': 'GV14', 'value': 0, 'uom': 22},     # cloud conditions
            {'driver': 'DISTANC', 'value': 0, 'uom': 83},  # visibility
            {'driver': 'SOLRAD', 'value': 0, 'uom': 74},   # solar radiataion
            {'driver': 'GV17', 'value': 0, 'uom': 56},     # aqi
            {'driver': 'GVP', 'value': 30, 'uom': 25},     # log level
            ]


