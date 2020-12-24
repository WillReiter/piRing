#!/usr/bin/env python3

from rpi_ws281x import PixelStrip, Color
import sys, os, time, datetime

#class piClock(PixelStrip):
#        def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
#            brightness=255, channel=0, strip_type=None, gamma=None)
#            super.()

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

def clock(params):
    # do clock things here
    
    # get system time
    # check for min/hour transition
    #   update LEDS or show animation
    # show
    pass

def static(params):
    # do static infinity mirror things here
    # pull functions straight from strandtest.py
    # take in a dict of animations & times to rotate?
    pass

def main():
    
    # Default LED strip configuration:
    LED_COUNT = 60        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    white = Color(127, 127, 127)
    red = Color(255, 0, 0)
    blue = Color(0, 255, 0)
    green = Color(0, 0, 255)

    #params = read_settings()

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    strip.begin()

    colorWipe(strip, white, 50)
        
    colorWipe(strip, red, 50)

    colorWipe(strip, blue, 50)

    colorWipe(strip, green, 50)

    colorWipe(strip, Color(0, 0, 0), 50)

    if clock:
        clock(params)
    elif static:
        static(params)
    elif game:
        wheelOfFortune()

def systemboot():
    # check if WIFI is configured and connected
    # ping NTP to confirm that's all good
        # if not, fall back to AP mode + static pattern / status LEDs
    main()
    pass

if __name__ == "__main__":
    systemboot()