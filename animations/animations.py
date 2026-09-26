from rpi_ws281x import Color
import time

colors = {
    "WHITE":        Color(127, 127, 127),
    "RED":          Color(255, 0, 0),
    "ORANGE":       Color(255, 69, 0),
    "GOLD":         Color(255, 215, 0),
    "GREEN":        Color(0, 255, 0),
    "BLUE":         Color(0, 0, 255),
    "LIGHT_BLUE":   Color(0, 191, 255),
    "MIDNIGHT_BLUE":Color(25, 25, 112),
    "INDIGO":       Color(75, 0, 130),
    "VOILET":       Color(238, 130, 238),
    "DARK_MAGENTA": Color(139, 0, 139),
    "PINK":         Color(255, 20, 147),
    "BLACK":        Color(0, 0, 0),
}


#################################################
### Utility
#################################################


def colorWipe(strip, color, wait_ms=10, reversed=False, start=None, stop=None):
    if start is None:
        start = 0
    if stop is None:
        stop = strip.numPixels()

    if not reversed:
        for i, j in enumerate(range(start, stop)):
            strip.setPixelColor(j, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
    else:
        for i, j in enumerate(range(start, stop)):
            strip.setPixelColor(stop - i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)


def colorFill(strip, color, start=None, stop=None):
    if start is None:
        start = 0
    if stop is None:
        stop = strip.numPixels()

    for i in range(start, stop):
        strip.setPixelColor(i, color)


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


#################################################
### General animations
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
            strip.setPixelColor(
                strip.numPixels() - (i + 1),
                wheel((int(i * 256 / strip.numPixels()) + j) & 255),
            )
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
### Clock drawing
#################################################


def drawClock(strip, now):
    strip.clear()
    drawMinute(strip, now, strip.color1, fill=True)
    drawHourTicks(strip, strip.color2)
    drawHour(strip, now, strip.color3)

    if abs((now.hour % 12) * strip.numPixels() / 12 - now.minute) <= 1:
        drawMinute(strip, now, strip.color1, fill=False)

    strip.setPixelColor(now.second, strip.color0)


def drawHourTicks(strip, color):
    for k in range(0, strip.numPixels(), int(strip.numPixels() / 12)):
        strip.setPixelColor(k, color)


def drawHour(strip, now, color):
    hour = now.hour % 12
    hour_pixel = hour * 5

    if hour_pixel - 1 < 0:
        strip.setPixelColor(hour_pixel + 59, color)
    else:
        strip.setPixelColor(hour_pixel - 1, color)

    strip.setPixelColor(hour_pixel, color)
    strip.setPixelColor(hour_pixel + 1, color)


def drawMinute(strip, now, color, fill=True):
    if fill:
        for j in range(now.minute + 1):
            strip.setPixelColor(j, strip.color1)
    else:
        strip.setPixelColor(now.minute, strip.color1)


#################################################
### Clock transition animations
#################################################


def animateClockStartup(strip, now, wait_ms):
    strip.clear()
    colorWipe(strip, strip.color1, wait_ms)

    for i, j in enumerate(range(now.minute, strip.numPixels())):
        strip.clear()
        drawHourTicks(strip, strip.color2)
        colorFill(strip, strip.color1, start=0, stop=int(strip.numPixels()) - i)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def hourChangeAnimation(strip, now, last, animation):
    if animation == "ping":
        for i in range(strip.numPixels()):
            drawClock(strip, now)
            strip.setPixelColor(i, strip.color1)
            strip.show()
            time.sleep(0.01)
    elif animation == "pong":
        for i in range(strip.numPixels()):
            drawClock(strip, last)
            strip.setPixelColor(strip.numPixels() - i, strip.color1)
            strip.show()
            time.sleep(0.01)
    elif animation == "flavortown":
        colorWipe(strip, colors["BLACK"], reversed=True)
        drawHourTicks(strip, strip.color2)
        strip.show()
        for j in range(256):
            for i in range(strip.numPixels()):
                drawHour(strip, now, wheel((i + j) & 255))
            strip.show()
            time.sleep(10 / 1000.0)


def minuteChangeAnimation(strip, now, last, animation):
    if animation == "ping":
        length = strip.numPixels() + 1
        for i in range(length):
            drawClock(strip, now)
            strip.setPixelColor(i, strip.color0)
            strip.show()
            time.sleep(1 / length)
    elif animation == "pong":
        length = strip.numPixels() - (now.minute + 1)
        for i in range(length):
            drawClock(strip, last)
            strip.setPixelColor(strip.numPixels() - i, strip.color1)
            strip.show()
            time.sleep(1 / length)
    elif animation == "crisscross":
        length = strip.numPixels()
        for i in range(length):
            drawClock(strip, now)
            strip.setPixelColor(i, strip.color0)
            strip.setPixelColor(length - i, strip.color0)
            strip.show()
            time.sleep(1 / length)
