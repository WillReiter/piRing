import os

try:
	os.system('sudo systemctl stop dhcpcd.service')
	os.system('sudo dhcpcd --nohook wpa_supplicant')
	os.system('sudo systemctl start dhcpcd.service dnsmasq.service hostapd.service')
except:
	os.system('sudo systemctl reboot')
