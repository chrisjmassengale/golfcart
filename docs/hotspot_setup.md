# Jetson WiFi Hotspot Setup

Configure the Orin Nano Super to broadcast its own WiFi network for
untethered field use (backyard training, course testing).

## Why
- No router needed on the course
- Phone connects directly to Jetson's network
- Web interface works anywhere

## Setup (when ready)

### 1. Install hostapd and dnsmasq
```bash
sudo apt-get install hostapd dnsmasq -y
```

### 2. Static IP on wlan0
Add to /etc/dhcpcd.conf:
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
### 3. dnsmasq config (/etc/dnsmasq.conf)
### 3. dnsmasq config (/etc/dnsmasq.conf)
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
### 4. hostapd config (/etc/hostapd/hostapd.conf)

interface=wlan0
ssid=GolfCart
wpa_passphrase=golfcart123
wpa=2
### 5. Connect
Phone joins "GolfCart" network, hits http://192.168.4.1:5000
