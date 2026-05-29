# Jetson WiFi Hotspot Setup

Configure Orin Nano Super to broadcast its own WiFi network for
untethered field use (backyard training, course testing).

## Setup

### 1. Install
sudo apt-get install hostapd dnsmasq -y
sudo systemctl stop hostapd dnsmasq

### 2. Static IP (/etc/dhcpcd.conf)
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant

### 3. DHCP (/etc/dnsmasq.conf)
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h

### 4. hostapd (/etc/hostapd/hostapd.conf)
interface=wlan0
ssid=GolfCart
wpa_passphrase=golfcart123
wpa=2
hw_mode=g
channel=7

### 5. Enable
sudo systemctl unmask hostapd
sudo systemctl enable hostapd dnsmasq
sudo systemctl start hostapd dnsmasq

## Connect
Phone/iPad joins "GolfCart" network → http://192.168.4.1:5000
Range: ~150ft line of sight
