# coding=utf-8

import os
import subprocess
import requests
import plotly
import time
import http.server
import socketserver
import threading
import plotly.graph_objs as go
from datetime import datetime
from config import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))


# write to file function
def filewrite(filename, mode, string):
    try:
        f = open(filename, mode)
        f.write(str(string))
        f.close()
    except Exception as e:
        filewrite(filename, 'a', 'Error: File write' + e)


filewrite(
    log_file,
    'a',
    '\n\t PiPing raised up\n' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if gpiomode:
    filewrite(log_file, 'a', 'Mode: GPIO MODE')
    import RPi.GPIO as GPIO  # Import GPIO library


# main ping function
def ping(hostname):
    try:
        # ping command
        pingcmd = "ping -c 1 " + hostname + \
            " | tail -1 | awk \'{print $4}\' | cut -d '/' -f 2 "
        # get ping stdout
        response = subprocess.run(pingcmd, shell=True, stdout=subprocess.PIPE)
        pingresponse = response.stdout.decode('utf-8')
        pingtime = pingresponse.split('.')[0]
        # get ping time
        if pingtime.isdigit():
            pingtimenum = int(pingtime)
            return pingtimenum
        else:
            filewrite(log_file, 'a', '\nE: Error while pinging!')
            return None

    # Error in pinging
    except Exception as e:
        filewrite(log_file, 'a', '\nE: Error while pinging ' + e)
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
        except Exception as e:
                return False
                filewrite(log_file, 'a', '\nE: No Connection ' + e)


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


class HttpThread(threading.Thread):

    def run(self):
        httpd = socketserver.TCPServer(("", http_port), Handler)
        httpd.serve_forever()


if __name__ == '__main__':
    timeplot = []
    plotdata = []
    cplot = []
    n = 0


    if http_server:
        # add http handler
        Handler = http.server.SimpleHTTPRequestHandler
        # run http server on port
        HttpThread().start()
        filewrite(log_file, 'a', '\nplot on http://localhost:' + str(http_port))
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
                    if gpiomode:
                        blink(redpin, 0.5, 2)
            elif server.type == 'offline':
                pingnum = ping(server.ip)
                server.ping.append(pingnum)
                if gpiomode and pingnum:
                    blink(bluepin, 0.3, 1)

            else:
                filewrite(log_file, 'a', '\nE: Server type error ')

        if n % plottime == 0:
            plotdata.clear()
            for server in serverslist:
                plotdata.append(go.Scatter(
                    x=timeplot,
                    y=server.ping,
                    mode='lines+markers',
                    name=server.name
                    ))
            # condition plot
            conditionplot = go.Scatter(
                x=timeplot,
                y=cplot,
                mode='lines',
                name='condition'
            )
            plotdata.append(conditionplot)
            plotlayout = dict(title='Ping Graph')
            plotinput = dict(data=plotdata, layout=plotlayout)

            # drow plot
            plot = plotly.offline.plot(plotinput, filename='index.html', auto_open=False)
            filewrite(log_file, 'a', '\nPlot: ' + plot)

            if n % reset == 0:
                for server in serverslist:
                    server.ping.clear()
                timeplot.clear()
                cplot.clear()
                n = 0
