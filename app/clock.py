#!/usr/bin/env python3

from rpi_ws281x import PixelStrip, Color
import sys, os, time
from datetime import datetime


#Global Attributes to be used across script. Initialized to 0
#add color constants here

#class PixelRing(PixelStrip):
#        def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
#            brightness=255, channel=0, strip_type=None, gamma=None, rotation=None)
#            super.()
#    
#    
#    override? the follwoing to inlcude rotation:
#    def setPixelColor(self, n, color):
#    def setPixelColorRGB(self, n, red, green, blue, white=0):
#    def getPixelColor(self, n):
#    def getPixelColorRGB(self, n):
#

def colorWipe(strip, color, wait_ms=100):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def read_settings():
    #import settings from YAML file
    #return session settings
    return 1

def drawClock(strip, time, COLOR_0, COLOR_1, COLOR_2, COLOR_3):
    
    #clear display first
    for i in range(60):
                strip.setPixelColor(i, Color(0, 0, 0))

    #update time: 
    for j in range(time.minute+1):
        strip.setPixelColor(j, COLOR_1)
    for k in range(0, 60, 5):
        strip.setPixelColor(k, COLOR_3)

    strip.setPixelColor(time.second, COLOR_0)
    

    # do clock things here
    
    #draw static hours with color_0

    #draw second with color_1

    #draw minutes with COLOR_2
    
    #draw hours with COLOR_3
    #
    # show
    return 0

def static(params):
    # do static infinity mirror things here
    # pull functions straight from strandtest.py
    # take in a dict of animations & times to rotate?
    pass

def main():
    
    DEBUG = False

    # Default LED strip configuration:
    LED_COUNT = 60        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    #replace with file i/o
    COLOR_0 = Color(127, 127, 127) #WHITE
    COLOR_1 = Color(255, 0, 0)      #GRN
    COLOR_2 = Color(0, 255, 0)      #RED
    COLOR_3 = Color(0, 0, 255)      #BLUE

    #params = read_settings()

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    strip.begin()

    colorWipe(strip, COLOR_0, 10)
        
    #colorWipe(strip, red, 50)

    #colorWipe(strip, blue, 50)

    #colorWipe(strip, green, 50)

    colorWipe(strip, Color(0, 0, 0), 10)

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
            time.sleep(1)

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