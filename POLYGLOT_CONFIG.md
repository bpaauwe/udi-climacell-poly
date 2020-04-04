The AERIS weather node server has the following user configuration
parameters:

- ClientID     : Your AERIS client ID to identify this application's requests.

- ClientSecret : Your AERIS client secret key, needed to authorize connection to the AERIS API.

- Forecast Days: The number of days of forecast data to track.

- Units        : 'metric' or 'imperial' request data in this units format.

- Location : 
	- by coordinates (latitude,longitude)  Ex.  37.25,-122.25
	- by city,state                        Ex.  seattle,wa
	- by city,state,country                Ex.  seattle,wa,us
	- by city,country                      Ex.  paris,france
	- by zip/postal code                   Ex.  98109
	- by 3 character IATA airport codes    Ex.  ROA
	- by NOAA public weather zone          Ex.  MNZ029
	- by PWS Station                       Ex.  PWS_VILLONWMR2

- Elevation    : Height above sea level, in meters, for the location specified above. 

- Plant Type   : Crop coefficent for evapotranspiration calculation. Default is 0.23

