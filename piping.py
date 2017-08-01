# coding=utf-8

import subprocess
import requests
import plotly
import time
import plotly.graph_objs as go
from datetime import datetime


serverslist = []


class servers:

    def __init__(self, name, ip, type, gpio):
        self.name = name
        self.ip = ip
        self.type = type
        self.gpio = gpio
        self.ping = []
        serverslist.append(self)


# server config
# name = servers('server name', 'ip', 'ping in offline/online',
# 'enable GPIO (on raspberrypi) check with condition True/False')
google = servers('Google', '8.8.8.8', 'online', True)
modem = servers('DSL', '192.168.1.1', 'offline', False)
router = servers('mikrotik', '10.0.0.1', 'offline', False)
verizon = servers('Verizon', '4.2.2.4', 'online', False)


# config
condition = 150  # condition to comparison
net_status_server = 'http://icanhazip.com'  # check conection  to net
sleeptime = 1  # sleep between each ping (second)
reset = 5000   # reset data plot after this time (Natural numbers)
plottime = 10  # drow plot after this time (Natural numbers)
gpiomode = False  # enable on raspberrypi (True/Flase)
greenpin = 7  # gpio pin conected to Green LED on BOARD mode
redpin = 3  # gpio pin conected to Red LED on BOARD mode
bluepin = 10  # gpio pin conected to Blue LED on BOARD mode


if gpiomode:
    import RPi.GPIO as GPIO  # Import GPIO library


# main ping function
def ping(hostname):
    try:
        # ping command
        pingcmd = "ping -c 1 " + hostname + " | tail -1 | awk \'{print $4}\' | cut -d '/' -f 2 "
        # get ping stdout
        response = subprocess.run(pingcmd, shell=True, stdout=subprocess.PIPE)
        pingresponse = response.stdout.decode('utf-8')
        pingtime = pingresponse.split('.')[0]
        # get ping time
        if pingtime.isdigit():
            pingtimenum = int(pingtime)
            return pingtimenum
        else:
            print('Error while pinging!')
            return None

    # Error in pinging
    except:
        print('Error while pinging!')
        return None


# check internet connection
def net_status(net_status_server):
        # check internet connection
        try:
            netstat = requests.get(net_status_server, timeout=1).status_code
            if netstat == 200:
                return True
            else:
                return False
                if gpiomode:
                    blink(redpin, 0.3, 2)
        except:
                return False


def blink(pin, timeon, number):
    # Use board pin numbering
    GPIO.setmode(GPIO.BOARD)
    # set warning
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    for i in range(0, number):
        GPIO.output(pin, True)
        time.sleep(timeon)
        GPIO.output(pin, False)
        time.sleep(timeon)


if __name__ == '__main__':
    timeplot = []
    plotdata = []
    cplot = []
    n = 0

    while True:
        time.sleep(sleeptime)

        n += 1
        # send ping time to x list for plot
        timeplot.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        cplot.append(condition)

        for server in serverslist:
            if server.type == 'online':
                if net_status(net_status_server):
                    pingnum = ping(server.ip)
                    server.ping.append(pingnum)
                    if server.gpio and gpiomode and pingnum:
                        if pingnum <= condition:
                            blink(greenpin, 0.3, 1)
                        elif pingnum > condition:
                            blink(redpin, 0.3, 1)
                else:
                    server.ping.append(None)
            elif server.type == 'offline':
                pingnum = ping(server.ip)
                server.ping.append(pingnum)
                if gpiomode and pingnum:
                    blink(bluepin, 0.3, 1)

            else:
                print('server type Error')

        if n % plottime == 0:
            plotdata.clear()
            for server in serverslist:
                plotdata.append(go.Scatter(
                    x = timeplot,
                    y = server.ping,
                    mode = 'lines+markers',
                    name = server.name
                    ))
            # condition plot
            conditionplot = go.Scatter(
                x = timeplot,
                y = cplot,
                mode = 'lines',
                name = 'condition'
            )
            plotdata.append(conditionplot)
            plotlayout = dict(title = 'Ping Graph')
            plotinput = dict(data=plotdata, layout=plotlayout)

            # drow plot
            plot = plotly.offline.plot(plotinput, filename='ping-graph.html', auto_open=False)
            print('plot: ' + plot)

            if n % reset == 0:
                for server in serverslist:
                    server.ping.clear()
                timeplot.clear()
                cplot.clear()
                n = 0
