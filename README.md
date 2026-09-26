# piRing
Application for Raspberry Pi + LED strip applications

**./app/clock.py**
* Main program for LED and clock control
* Uses RPI system time for clock time
* Pulls settings from settings.txt
* Pulls color profile from colors.txt
* Pulls animation list from animations.txt
* Auto-run on startup
* Includes:
* Boot sequence / LED test
* Determines mode (clock vs static)
* Begins display ASAP
* Continues to operate, even in AP mode
* Link to HTML to show color / animation changes live?
* Not sure how to do this...

**./web/interface.html**
* Basic web app used to change user settings of clock
* Served via captive portal and/or static IP once RPI is in AP mode
* Reads wifi SSIDs, allows user to enter credentials, writes to wpa_supplicant.conf
* Reads profiles from color_profiles.txt, takes user selection of profile, writes selected profile to color.txt
* Optional color wheel selection to save custom profile to color_profiles.txt, refresh list and allow user to select that profile

**./profiles/active/colors.txt**
Structure:

```
[profile name]
	<<hourTick_RGB>>
	<<currentHour_RGB>>
	<<minuteFill_RGB>>
	<<currentMinute_RGB>>
```

* R/W
* Will be regenerated if deleted or corrupted

**./profiles/idle/color_profiles.txt**
* List of color profiles. Some preloaded, some user configured
* Used to feed colors.txt - same structure but repeated
* R/W

**./profiles/active/animations.txt**
* Trigger/animation pairs
* Structure:

```
[trigger type]
	<<animation_to_use>>
 ```
 
* R/W
* Will be regenerated if deleted or corrupted

**./profiles/idle/animation_profiles.txt**
* Available animations for various triggers
* Handles both clock and static modes
* All animations and triggers have corresponding functions in clock.py

Structure:

```
[trigger type]
	<<available_animation_0>>
	<<available_animation_1>>
 ```
 
**./profiles/settings.txt**
* Set of flags and values used for miscellaneous settings. 
* Example settings:
* Time offset
* Time refresh rate
* Extra WLAN settings, if applicable
* SW update URL
* Clock vs static mode

**./profiles/.settings.default.txt**
* Factory default settings for settings.txt
* Read only


**./utils/setAP.py**
* Used to change the RPi from a DHCP client to an AP on wlan0
* Triggered by button push on device

**./utils/color_handler.py**
* Used to manage R/W of colors.txt and color_profiles.txt
* Not sure if this is necessary or if the HTML can just handle the I/O

**./.deps.txt**
* Current list of dependencies. 
* To be replaced with installer / venv requirements list.


**/etc/wpa_supplicant/wpa_supplicant.conf**
* Configuration file for wifi access settings
* Standard config file for RPI
* TBD - will likely keep local copy and add path to RPI
