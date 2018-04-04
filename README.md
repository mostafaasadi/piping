# About PiPing
This is a Python script which pings your desired IPs and generates a plot, showing target up-time based on received replies.
The plot is generated as a standard HTML file which is view-able in any standard web browser.
Furthermore, if you are running this script on RaspberryPi or compatible SBC, it is possible to connect an RGB LED to RPi's GPIO
to show server status. For example, LED will be turned Green if the server is up and red if un-accessible. LED colors/blinking is
user configurable.

![piping](https://raw.githubusercontent.com/mostafaasadi/piping/master/screenshot.png)

# Installation
- `pip3 install plotly`
- `pip3 install requests`
- `pip3 install subprocess`
- `git clone https://github.com/mostafaasadi/piping`
- `cd piping`
- `nohup python3 piping.py &`
- you can also create systemd unit to manage PiPing:

 - make `/etc/systemd/system/piping.service` with the following contents

   for first run: `sudo systemctl daemon-reload `

   and manage with :

   `sudo systemctl enable`
   `sudo systemctl start`
   `sudo systemctl stop`


```
[Unit]
Description=PiPing service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/mostafa/piping/piping.py
WorkingDirectory=/home/mostafa/piping
Restart=always
RestartSec=2

[Install]
WantedBy=sysinit.target
```


# Configuration
To change IPs (add/remove/edit) `config.py`
```
name = servers(
'server name',
'ip',
'ping in offline/online',
'enable GPIO (on raspberrypi) check with condition True/False (recommanded: enable for IPs outside your LAN)')
```
and other configurations.

## RaspberryPi GPIO activation
If you are running piping on RaspberryPi, enable `gpiomode` on `config.py`. Then connect RGB LED according to this diagram:
![piping](https://raw.githubusercontent.com/mostafaasadi/piping/master/physical-pin-numbers.png)
finally set `redpin`,`greenpin` and `bluepin` in configuration section.

# Usage
**piping** creates the plot as `index.html` and updates it according to settings and if you set `http_server` , `True` show it on your raspberrypi ip:`http_port`.

for example : `10.0.0.214:8008`

If you are running piping on RaspberryPi or compatible SBC, it is possible to turn on `gpiomode` and blink an RGB LED with user
configurable setting interactively. Blue color is usually used for IPs of devices in your LAN (e.g. routers).
Red and Green LEDs could be turned on or blinked using multiple conditions.

Please refer to the comments in configuration section
for more information.
