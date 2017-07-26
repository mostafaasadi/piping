import RPi.GPIO as GPIO ## Import GPIO library
import subprocess,time,requests,plotly
import plotly.graph_objs as go
# from datetime import datetime TODO

# coding=utf-8

# Use board pin numbering
GPIO.setmode(GPIO.BOARD)

#set warning
GPIO.setwarnings(False)


## you can use input
# hostname = input('hostname: ')
# local = input('local: ')
# condition = input('condition: ')
# testserver = input('test server: ')

## or just static value
hostname = '8.8.8.8'
local = '10.0.0.1'
condition = '145'
testserver = 'http://icanhazip.com'

# variable
yplot = []
xplot = []
lpp = []
n = 0

# main ping function
def check_ping(hostname):
    try:
        # ping command
        pingcmd = "ping -c 1 " + hostname + " | tail -1 | awk \'{print $4}\' | cut -d '/' -f 2 "
        # get ping stdout
        response = subprocess.run(pingcmd,shell=True,stdout=subprocess.PIPE)
        pingtime = response.stdout.decode('utf-8')
        # get ping time
        pingtimenum = pingtime.split('.')[0]
        return pingtimenum

    # Error in pinging
    except:
        print('Error!')
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)
        time.sleep(0.3)
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)

GPIO.setup(7, GPIO.OUT) # Setup GPIO Pin 7 to OUT , Green LED
GPIO.setup(3, GPIO.OUT) # Setup GPIO Pin 3 to OUT , Red LED
GPIO.setup(10, GPIO.OUT) # Setup GPIO Pin 10 to OUT , Blue LED

# main loop
while True:
    # sleep between each ping
    time.sleep(0.5)

    # loop counter
    n += 1
    # send ping number to x list for plot
    xplot.append(n)

    # ping local router
    localpingtimenum = check_ping(local)
    print(local + ' :: ' + localpingtimenum)
    if localpingtimenum.isdigit():
        # send local ping to lpp list for plot
        lpp.append(int(localpingtimenum))

    # blink blue LED if router is available
    if localpingtimenum :
        GPIO.output(10,True)
        time.sleep(0.1)
        GPIO.output(10,False)

    # blink Red LED if router is not available
    else :
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)
        time.sleep(0.3)
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)
        print('local is not available')


    # sleep between local and server ping
    time.sleep(0.3)

    # check internet connection
    try:
        netstat = requests.get(testserver,timeout=1).status_code
        if netstat == 200 :
            status = True
    except:
        status = False
        print('internet is not reachable')

    if status :
        # check server ping
        pingtimenum = check_ping(hostname)
        print(hostname + ' :: ' + pingtimenum)

        if pingtimenum.isdigit():
            # blink Green LED for low ping
            if int(pingtimenum) < int(condition) :
                print("green")
                GPIO.output(7,True)
                time.sleep(0.1)
                GPIO.output(7,False)
            # blink Red LED for high ping
            elif int(pingtimenum) > int(condition) :
                print("red")
                GPIO.output(3,True)
                time.sleep(0.1)
                GPIO.output(3,False)

            # send server ping for plot
            yplot.append(int(pingtimenum))

        # creat plot every 10 ping
        if n%10 == 0 :
            # local ping plot
            localplot = go.Scatter(
                x = xplot,
                y = lpp,
                mode = 'lines+markers',
                name = 'local ping'
            )
            # server ping plot
            serverplot = go.Scatter(
                x = xplot,
                y = yplot,
                mode = 'lines+markers',
                name = hostname
            )
            plotdata = [localplot,serverplot]
            plotlayout = dict(title = 'Ping Graph')
            plotinput = dict(data=plotdata, layout=plotlayout)

            # drow plot
            plot = plotly.offline.plot(plotinput, filename='ping-graph.html',auto_open=False)
            print('plot: ' + plot)


    # internet connection is not reachable
    else:
        print('unreachable')
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)
        time.sleep(0.3)
        GPIO.output(3,True)
        time.sleep(0.3)
        GPIO.output(3,False)
