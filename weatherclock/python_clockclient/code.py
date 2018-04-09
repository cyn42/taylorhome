import board
import neopixel
import time
import grid
import esp_network_connect
import wcclient_config as config
import socket
 
pixpin = board.GPIO14
numpix = 60
strip = neopixel.NeoPixel(pixpin, numpix, brightness=0.6, auto_write=False)

def connect_wifi():
    wifi_pos = grid.get_icon('wifi')
    set_colors_on_strip(wifi_pos, (255,165,0))
    esp_network_connect.do_connect()
    if esp_network_connect.is_connected():
            set_colors_on_strip(wifi_pos, (0,0,255))
    if not esp_network_connect.is_connected():
        set_colors_on_strip(wifi_pos, (255,0,0))

def set_colors_on_strip(positions,color):
    for pos in positions:
        strip[pos] = color
    strip.show()

connect_wifi()

print('Weather URL: ',config.WEATHERSERVER['url'])

#response = esp_network_connect.http_get(config.WEATHERSERVER['url'],config.WEATHERSERVER['port'])

#print(response)

weather_coords = grid.get_grid_coords('tomorrow_high','dummy','dummy','dummy','dummy')
set_colors_on_strip(weather_coords,(0,255,0))