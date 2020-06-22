
# Climacell weather service

This is a node server to pull weather data from the Climacell weather network and make it available to a [Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)

(c) 2020 Robert Paauwe
MIT license.

Go to the [Climacell](http://www.climacell.co) website for more information the Climacell weather network.


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
   * How often to poll the climacell weather service for current condition data (in seconds). 
#### Long Poll
   * How often to poll the climacell weather service for forecast data (in seconds). Note that the data is only updated every 10 minutes. Setting this to less may result in exceeding the free service rate limit.
#### APIKey
   * Your Climacell API key needed to authorize the connection the the climacell API.
#### Latitude
   * Specify the latitude of the location to use in the weather data queries (in decimal degrees).  
#### Longitude
   * Specify the longitude of the location to use in the weather data queries (in decimal degrees).  
#### Elevation
   * The elevation of your location, in meters. This is used for the ETo calculation.
#### Forecast Days
   * The number of days of forecast data to track (0 - 15).
#### Plant Type
   * Used for the ETo calculation to compensate for different types of ground cover. Default is 0.23
#### Units
   * set to 'us' or 'si' to control which units are used to display the weather data.

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
 * sys.node.[address].GV13    (current weather conditions)
 * sys.node.[address].GV14    (current percent cloud coverage)
 * sys.node.[address].GV6     (current precipitation accumulation)
 * sys.node.[address].GV2     (current feels like temperature)
 * sys.node.[address].GV9     (current moon phase)
 * sys.node.[address].GV17    (current air quality)

### Forecast node
 * sys.node.[address].CLIHUM  (forecasted humidity)
 * sys.node.[address].BARPRES (forecasted barometric pressure)
 * sys.node.[address].RAINRT  (forecasted rain rate)
 * sys.node.[address].GV6     (forecasted precipitation)
 * sys.node.[address].GV18    (forecasted chance of precipitation)
 * sys.node.[address].GV19    (day of week forecast is for)
 * sys.node.[address].GV0     (forecasted high temperature)
 * sys.node.[address].GV1     (forecasted low temperature)
 * sys.node.[address].GV13    (forecasted weather conditions)
 * sys.node.[address].GV7     (forecasted max wind speed)
 * sys.node.[address].GV8     (forecasted min wind speed)
 * sys.node.[address].GV20    (calculated ETo for the day)

## Requirements
1. Polyglot V2.
2. ISY firmware 5.0.x or later
3. An account with Climacell weather (http://www.climacell.co/pricing)

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "AERIS Weather".

Then restart the climacell nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 1.0.5 06/22/2020
   - Correct pressure range/precision.
- 1.0.4 04/11/2020
   - Fix typo in forecast error message.
   - Don't convert metric wind speed for ETo calc.
- 1.0.3 04/11/2020
   - Change current condition precipitation to precipitation rate.
- 1.0.2 04/11/2020
   - Fix bugs with number of forecast days.
- 1.0.1 04/10/2020
   - Change the max number of forecast days to 15.
- 1.0.0 04/09/2020
   - Initial version published to github.
