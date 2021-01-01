#!/usr/bin/env python3

from rpi_ws281x import PixelStrip, Color
import sys, os, time
from datetime import datetime

#################################################
### Constants to be used across script.
#################################################

WHITE =         Color(127, 127, 127)
RED =           Color(255, 0, 0)
ORANGE =        Color(255, 69, 0)
GOLD =          Color(255, 215, 0)
GREEN =         Color(0, 255, 0)
BLUE =          Color(0, 0, 255)
LIGHT_BLUE =    Color(0, 191, 255)
INDIGO =        Color(75, 0, 130)
VOILET =        Color(238, 130, 238)
PINK =          Color(255, 20, 147)
BLACK =         Color(0, 0, 0)
#ALL_COLORS = []

#################################################
### PixelRing class
#################################################

class PixelRing(PixelStrip):

    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0, strip_type=None, gamma=None, rotation=0):
        super().__init__(num, pin, freq_hz, dma, invert, brightness, channel, strip_type, gamma)
        
        self.rotation = rotation
    
    def clear(self):
        for i in range(self.numPixels()):
            self._led_data[i] = Color(0,0,0)

    # override the follwoing to inlcude rotation:
    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        n = (n + self.rotation) % int(self.numPixels())
        self._led_data[n] = color
            
    # other methods that will need an override to include rotation, if used
    # def setPixelColorRGB(self, n, red, green, blue, white=0):
    # def getPixelColor(self, n):
    # def getPixelColorRGB(self, n):

#################################################
### Pixel fill functions
#################################################

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

def colorFill(strip, color, start=None, stop=None):
    if start == None:
        start = 0
    if stop == None:
        stop = strip.numPixels()

    for i in range(start, stop):
        strip.setPixelColor(i, color)

#################################################
### "Static" Animations
#################################################

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=10, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(strip.numPixels() - (i + 1), wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

#################################################
### Clock-specific animations
#################################################

def animateClockStartup(strip, now, wait_ms, min_Color, hourTick_Color):
    strip.clear()
    colorWipe(strip, min_Color, wait_ms)

    for i, j in enumerate(range(now.minute, strip.numPixels())):
        strip.clear()
        drawHourTicks(strip, hourTick_Color)
        colorFill(strip, min_Color, start=0, stop=int(strip.numPixels())-i)
        strip.show()
        time.sleep(wait_ms/1000.0)        

#################################################
### Clock-specific functions
#################################################

def drawClock(strip, time, COLOR_0, COLOR_1, COLOR_2, COLOR_3):
    
    #clear display first
    strip.clear()

    #update minute fill: 
    for j in range(time.minute+1):
        strip.setPixelColor(j, COLOR_1)
    
    drawHourTicks(strip, COLOR_2)

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

def drawHourTicks(strip, color):
    #update hour ticks
    for k in range(0, strip.numPixels(), int(strip.numPixels()/12)):
        strip.setPixelColor(k, color)

#################################################
### State Machine functions
#################################################

def importSettings():
    #import settings from YAML file
    #return session settings
    return 1

def init():
    pass

def main():
    
    DEBUG = False

    #parse arguments here (if any alowed)

    #params = read_settings() from yaml

    if DEBUG:
        #print(help(PixelStrip))
        pass
    
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

    # check if WIFI is configured and connected
    # ping NTP to confirm that's all good
    # if not, fall back to AP mode + static pattern / status LEDs

    try:
    
        strip = PixelRing(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, rotation=ROTATION)

        strip.begin()

        rainbowCycle(strip, wait_ms=10, iterations=1)

        now = datetime.now()

        #initial animation here:
        animateClockStartup(strip, now, 10, COLOR_1, COLOR_2)

        
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

    except KeyboardInterrupt:
        colorWipe(strip, BLACK, 10, reversed=True)            

if __name__ == "__main__":
    main()