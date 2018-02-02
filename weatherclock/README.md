# Weather Clock

This is an implementation of a physical "clock" that shows current and upcoming 
weather conditions visually by lighting up the corresponding icons in a display.

It is based on Weather Icon Display by Jason Rolfe: https://hackaday.io/project/8323-weather-icon-display

## Key Components:

### Physical Clock

The components of the physical clock (so far - still under construction)

1. Adafruit Neopixel Strip, black 30 LEDs per meter: https://www.adafruit.com/product/1460
1. Adafruit Feather Huzzah flashed with Circuit Python: https://www.adafruit.com/product/2821
1. 1/8" Hardboard for mounting the lights, and laser cut with icons

watherclock.svg contains the vector template file for the laser cutter. I haven't tried it yet.
It is also in metric because I'm Canadian :D

### Software

The software implementation is in Python. 

Basic activity overview:

* Connect to Wifi (indicate progress and status using the WiFi icon)
* Connect to Open Weather Map (Requires urequests library on the micropython device: https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py)
    * Pull the current weather conditions
    * Pull the 5 day / 3 hr forecast in metric units
* Cycle through the 5 day forecast and sort into today / tonight / tomorrow summary buckets
* Update the display loop

The display loop will show conditions as follows:

1. Now (The current temperature and prevailing conditions)
1. Today Min (Will skip if it is currently after sunset): Minimum temperature for all forecasts falling in the "Today" bucket, prevailing condition, total precipitation
1. Today Max (Will skip if it is currently after sunset): Maximum temperature for all forecasts falling in the "Today" bucket, prevailing condition, total precipitation
1. Tonight Min
1. Tonight Max
1. Tomorrow Min
1. Tomorrow Max

Colors will be randomized for each icon. Icons will be identified by the sequence number of the LEDs that fall under it.