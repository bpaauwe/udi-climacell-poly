
# AERIS weather service

This is a node server to pull weather data from the AERIS weather network and make it available to a [Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)

(c) 2020 Robert Paauwe
MIT license.


## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in Polyglot Web
   * After the install completes, Polyglot will reboot your ISY, you can watch the status in the main polyglot log.
4. Once your ISY is back up open the Admin Console.
5. Configure the node server per configuration section below.

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to poll the AERIS weather service for current condition data (in seconds). Note that the PWS partner plan only allows for 1000 requests per day so set this appropriately.
#### Long Poll
   * How often to poll the AERIS weather service for forecast data (in seconds). Note that the data is only updated every 10 minutes. Setting this to less may result in exceeding the free service rate limit.
#### ClientID
	* Your AERIS client ID, needed to authorize the connection the the AERIS API.
#### ClientSecret
	* Your AERIS client secret key, needed to authorize the connection the the AERIS API.
#### Location
	* Specify the location to use in the weather data queries.  The location can be specified using the following conventions:
		- coordinates (latitude,longitude)  Ex.  37.25,-122.25
		- city,state                        Ex.  seattle,wa
		- city,state,country                Ex.  seattle,wa,us
		- city,country                      Ex.  paris,france
		- zip/postal code                   Ex.  98109
		- 3 character IATA airport codes    Ex.  ROA
		- NOAA public weather zone          Ex.  MNZ029
		- PWS Station                       Ex.  PWS_VILLONWMR2
#### Elevation
	* The elevation of your location, in meters. This is used for the ETo calculation.
#### Forecast Days
	* The number of days of forecast data to track (0 - 12). Note that the basic plan only provides 7 days of data.
#### Plant Type
	* Used for the ETo calculation to compensate for different types of ground cover. Default is 0.23
#### Units
	* set to 'imperial' or 'metric' to control which units are used to display the weather data.

## Node substitution variables
### Current condition node
 * sys.node.[address].ST      (Node sever online)
 * sys.node.[address].CLITEMP (current temperature)
 * sys.node.[address].CLIHUM  (current humidity)
 * sys.node.[address].DEWPT   (current dew point)
 * sys.node.[address].BARPRES (current barometric pressure)
 * sys.node.[address].SPEED   (current wind speed)
 * sys.node.[address].WINDDIR (current wind direction )
 * sys.node.[address].DISTANC (current visibility)
 * sys.node.[address].SOLRAD  (current solar radiation)
 * sys.node.[address].GV5     (current gust speed)
 * sys.node.[address].GV11    (current condition coverage)
 * sys.node.[address].GV12    (current intensity of conditions)
 * sys.node.[address].GV13    (current weather conditions)
 * sys.node.[address].GV14    (current percent cloud coverage)
 * sys.node.[address].GV6     (current precipitation accumulation)
 * sys.node.[address].GV2     (current feels like temperature)
 * sys.node.[address].GV3     (current heat index temperature)
 * sys.node.[address].GV4     (current wind chill temperature)

### Forecast node
 * sys.node.[address].CLIHUM  (forecasted humidity)
 * sys.node.[address].BARPRES (forecasted barometric pressure)
 * sys.node.[address].UV      (forecasted max UV index)
 * sys.node.[address].GV19    (day of week forecast is for)
 * sys.node.[address].GV0     (forecasted high temperature)
 * sys.node.[address].GV1     (forecasted low temperature)
 * sys.node.[address].GV11    (forecasted condition coverage)
 * sys.node.[address].GV12    (forecasted intensity of conditions)
 * sys.node.[address].GV13    (forecasted weather conditions)
 * sys.node.[address].GV14    (forecasted percent cloud coverage)
 * sys.node.[address].SPEED   (forecasted wind speed)
 * sys.node.[address].GV5     (forecasted gust speed)
 * sys.node.[address].GV6     (forecasted precipitation)
 * sys.node.[address].GV7     (forecasted max wind speed)
 * sys.node.[address].GV8     (forecasted min wind speed)
 * sys.node.[address].GV20    (calculated ETo for the day)

## Requirements
1. Polyglot V2.
2. ISY firmware 5.0.x or later
3. An account with AERIS weather (http://aerisweather.com)

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "AERIS Weather".

Then restart the AERIS nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 1.0.2 03/30/2020
   - Add snow depth to current conditions and forecasts
   - change "rain today" to "precipitation"
- 1.0.1 03/30/2020
   - Fix issues with the profile files.
- 1.0.0 03/18/2020
   - Initial public release
- 0.0.1 08/20/2019
   - Initial version published to github for testing
