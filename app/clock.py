#!/usr/bin/env python3

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# rpi_ws281x lives in the project venv; `sudo python3` drops it, so re-exec with the venv's interpreter
VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python3")
if os.path.exists(VENV_PYTHON) and sys.prefix != os.path.join(PROJECT_ROOT, ".venv"):
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

# Add project root to path so `animations` package is importable
sys.path.insert(0, PROJECT_ROOT)

from rpi_ws281x import PixelStrip, Color
import time
import signal
import json
from datetime import datetime
from animations import (
    colors,
    rainbowCycle,
    colorWipe,
    animateClockStartup,
    drawClock,
    hourChangeAnimation,
    minuteChangeAnimation,
)


#################################################
### PixelRing
#################################################


class PixelRing(PixelStrip):

    def __init__(self, clockConfig, colorConfig):
        super().__init__(
            num=clockConfig["size"],
            pin=clockConfig["pin"],
            freq_hz=clockConfig["frequency"],
            dma=clockConfig["dma"],
            invert=clockConfig["ledInvert"],
            brightness=clockConfig["brightness"],
            channel=clockConfig["ledChannel"],
        )
        self._started = False
        self.rotation = clockConfig["rotation"]
        self.color0 = colors[colorConfig["seconds"]]
        self.color1 = colors[colorConfig["minutes"]]
        self.color2 = colors[colorConfig["hour"]]
        self.color3 = colors[colorConfig["currentHour"]]

    def begin(self):
        super().begin()
        self._started = True

    def _cleanup(self):
        if self._started:
            super()._cleanup()

    def clear(self):
        for i in range(self.numPixels()):
            self[i] = Color(0, 0, 0)

    def setPixelColor(self, n, color):
        n = (n + self.rotation) % int(self.numPixels())
        self[n] = color


#################################################
### Signal handling
#################################################


def receiveSignal(signalNumber, frame):
    print("Received:", signalNumber)
    raise KeyboardInterrupt


#################################################
### Main
#################################################


def main():
    if os.getuid() != 0:
        print("Error: must be run as root for DMA/GPIO access.")
        print("Use: ./auto_start.sh")
        sys.exit(1)

    with open(f"{PROJECT_ROOT}/config/settings.json") as f:
        clockConfig = json.load(f)

    with open(f"{PROJECT_ROOT}/{clockConfig['colorPallett']}") as f:
        colorConfig = json.load(f)

    with open(f"{PROJECT_ROOT}/config/animations.json") as f:
        animationConfig = json.load(f)

    strip = PixelRing(clockConfig, colorConfig)
    strip.begin()

    print(clockConfig)

    try:
        rainbowCycle(strip, wait_ms=10, iterations=1)

        now = datetime.now()
        last = now

        animateClockStartup(strip, now, 10)

        while True:
            now = datetime.now()

            if last.hour != now.hour:
                hourChangeAnimation(strip, now, last, animationConfig["hour"])
            elif last.minute != now.minute and now.minute % 15 == 0:
                minuteChangeAnimation(strip, now, last, animationConfig["quarter"])
            elif last.minute != now.minute:
                minuteChangeAnimation(strip, now, last, animationConfig["minute"])

            drawClock(strip, now)
            strip.show()
            time.sleep(0.01)
            last = now

    except KeyboardInterrupt:
        colorWipe(strip, colors["BLACK"], 10, reversed=True)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, receiveSignal)
    main()
