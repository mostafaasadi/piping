# piping
ping and plot servers and hosts 
piping drow plot and blink (3color) LED on raspberrypi.

![piping](https://raw.githubusercontent.com/mostafaasadi/piping/master/screenshot.png)

# Install
- `pip3 install plotly`
- `pip3 install requests`
- `pip3 install subprocess`
- `git clone https://github.com/mostafaasadi/piping`
- `cd piping`
- `nohup python3 piping.py &`

# config
for change in servers(add/remove/edite) edite line 25-32
`` name = servers('server name',
'ip',
'ping in offline/online',
'enable GPIO (on raspberrypi) check with condition True/False (recommand : enable for one online server)') ``
and other config (line 34-43)

## GPIO mode 
if you run it on raspberrypi , enable `gpiomode` on line 40 and connect LED acording to this 
![piping](https://raw.githubusercontent.com/mostafaasadi/piping/master/physical-pin-numbers.png)
and config `redpin`,`greenpin` and `bluepin` in config section

# Usage 
**piping** creat a plot with name `ping-graph.html` and update it , also on `gpiomode` on raspberrypi it blink LEDs (blue for offline ping , green for less than `condition` , red for more than `condition` and duble red blink for no internet connection)
