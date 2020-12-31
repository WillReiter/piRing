#!/usr/bin/env python3

from rpi_ws281x import PixelStrip, Color
import sys, os, time
from datetime import datetime


#Global Attributes to be used across script. Initialized to 0
WHITE = Color(127, 127, 127)
RED = Color(255, 0, 0)
ORANGE = Color(255, 69, 0)
GOLD = Color(255, 215, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
LIGHT_BLUE = Color(0, 191, 255)
INDIGO = Color(75, 0, 130)
VOILET = Color(238, 130, 238)
PINK = Color(255, 20, 147)
BLACK =  Color(0, 0, 0)

#ALL_COLORS = 

class PixelRing(PixelStrip):

    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0, strip_type=None, gamma=None, rotation=0):
        super().__init__(num, pin, freq_hz, dma, invert, brightness, channel, strip_type, gamma)
        
        self.rotation = rotation
    
    # override the follwoing to inlcude rotation:
    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """

        n = (n + self.rotation) % int(self.numPixels())

        self._led_data[n] = color
    #   other methods that will need an override to include rotation, if used
    #    def setPixelColorRGB(self, n, red, green, blue, white=0):
    #    def getPixelColor(self, n):
    #    def getPixelColorRGB(self, n):


def colorWipe(strip, color, wait_ms=100, reversed=False, start=None, stop=None):
    
    #by default, sweep full strip
    if start == None:
        start = 0
    if stop == None:
        stop = strip.numPixels()

    # Wipe color across display a pixel at a time
    if not reversed:
        for i, j in enumerate(range(start,stop)):
            strip.setPixelColor(j, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
    else:
        for i, j in enumerate(range(start,stop)):
            strip.setPixelColor(stop-i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)

def startup_animation(strip, time):
    colorWipe(strip, WHITE, 10)
    colorWipe(strip, BLACK, 10, reversed=True, start=time.minute)


def read_settings():
    #import settings from YAML file
    #return session settings
    return 1

def drawClock(strip, time, COLOR_0, COLOR_1, COLOR_2, COLOR_3):
    
    #clear display first
    for i in range(60):
                strip.setPixelColor(i, BLACK)

    #update minute fill: 
    for j in range(time.minute+1):
        strip.setPixelColor(j, COLOR_1)
    
    #update hour ticks
    for k in range(0, 60, 5):
        strip.setPixelColor(k, COLOR_2)

    #update current hour
    hour = time.hour % 12
    hour_pixel = hour * 5

    if hour_pixel - 1 < 0:  
        strip.setPixelColor(hour_pixel + 59, COLOR_3)
    else:
        strip.setPixelColor(hour_pixel - 1, COLOR_3)

    strip.setPixelColor(hour_pixel, COLOR_3)
    strip.setPixelColor(hour_pixel + 1, COLOR_3)

    #update second
    strip.setPixelColor(time.second, COLOR_0)

    return 0

def static(params):
    # do static infinity mirror things here
    # pull functions straight from strandtest.py
    # take in a dict of animations & times to rotate?
    pass

def main():
    
    DEBUG = False

    if DEBUG:
        print(help(PixelStrip))
    
    # Default LED strip configuration:
    LED_COUNT = 60        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    ROTATION = 52

    #replace with file i/o
    COLOR_0 = WHITE                 #seconds
    COLOR_1 = GOLD                  #minute fill
    COLOR_2 = LIGHT_BLUE            #hour ticks
    COLOR_3 = BLUE                  #current hour

    #params = read_settings()

    strip = PixelRing(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, rotation=ROTATION)

    strip.begin()

    now = datetime.now()

    #initial animation here:
    startup_animation(strip, now)

    if True:
        while True:
            #get current time here
            now = datetime.now()

            if DEBUG:
                current_time = now.strftime("%H:%M:%S")
                print("Time: ", current_time)    

            drawClock(strip, now, COLOR_0, COLOR_1, COLOR_2, COLOR_3)
            strip.show()
            #drawClock(strip, time, COLOR_0, COLOR_1, COLOR_2, COLOR_3)
            #if hour change     
               # means do animation here
            #elif minute change
                # do animaiton here
            #check for stop condition /interrupt here
            time.sleep(.1)

    #elif static:
        #static(params)
    #elif game:
    #    wheelOfFortune()

def systemboot():
    # check if WIFI is configured and connected
    # ping NTP to confirm that's all good
        # if not, fall back to AP mode + static pattern / status LEDs
    main()
    pass

if __name__ == "__main__":
    systemboot()