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
log_file = 'pipinglog'
sleeptime = 1  # sleep between each ping (second)
reset = 5000   # reset data plot after this time (Natural numbers)
plottime = 10  # drow plot after this time (Natural numbers)
http_server = True  # enable/disable web server
http_port = 8000  # http port
gpiomode = False  # enable on raspberrypi (True/Flase)
greenpin = 7  # gpio pin conected to Green LED on BOARD mode
redpin = 3  # gpio pin conected to Red LED on BOARD mode
bluepin = 10  # gpio pin conected to Blue LED on BOARD mode
