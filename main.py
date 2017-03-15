#!/usr/bin/env python

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, render_template, request, redirect, url_for, flash, Response
from ConfigParser import SafeConfigParser
from werkzeug.datastructures import ImmutableOrderedMultiDict
from time import sleep
import CHIP_IO.GPIO as GPIO
import threading


app = Flask(__name__)
app.secret_key = "super secret key"


# Load the config file
config = SafeConfigParser()
configPath = 'usersettings.ini'


# list of all pins on CHIP
chip_io = ['TWI1-SDA', 'TWI1-SCK', 'LCD-D2', 'PWM0', 'LCD-D4', 'LCD-D3', 'LCD-D6', 'LCD-D5', 
            'LCD-D10', 'LCD-D7', 'LCD-D12', 'LCD-D11', 'LCD-D14', 'LCD-D13', 'LCD-D18', 
            'LCD-D15', 'LCD-D20', 'LCD-D19', 'LCD-D22', 'LCD-D21', 'LCD-CLK', 'LCD-D23', 
            'LCD-VSYNC', 'LCD-HSYNC', 'LCD-DE', 'UART1-TX', 'UART1-RX', 'LRADC', 'XIO-P0', 
            'XIO-P1', 'XIO-P2', 'XIO-P3', 'XIO-P4', 'XIO-P5', 'XIO-P6', 'XIO-P7', 'AP-EINT1', 
            'AP-EINT3', 'TWI2-SDA', 'TWI2-SCK', 'CSIPCK', 'CSICK', 'CSIHSYNC', 'CSIVSYNC', 
            'CSID0', 'CSID1', 'CSID2', 'CSID3', 'CSID4', 'CSID5', 'CSID6', 'CSID7']
            
# Live dictionary for states of pins    
pass_data = {}
pass_data['chip_pins'] = chip_io
pass_data['devices'] = {}


def get_devices(): # Starts first to build live dictionary
    GPIO.cleanup() # Clean up GPIO at start
    config.read(configPath) # Read the config file to get devices and settings
    zones = config.get('zones', 'zone_count') # Get the zone count from config
    for device in config.sections()[1:]: # loop through all devices in the config
        deviceData = {} # Nested dictionary for storing device options in the device dictionary
        for deviceOptions in config.options(device): # loop through all device options for the current device
            deviceData[deviceOptions] = config.get(device, deviceOptions) # Add device options to deviceData dictionary
        pass_data['devices'][device] = deviceData # Add device and deviceData to live dictionary
        pass_data['devices'][device]['state'] = 'Off' # Add a device dictionary to track the state of the device
    pass_data['zone_count'] = (int(zones)) # Add the number of zones from the config file
    setup_devices() # Setup devices after building live dictionary


def setup_devices(): # Initial setup for device pins on start
    for device in pass_data['devices']:
        if pass_data['devices'][device]['input_output'] == 'Input':
            input_setup(device)
        elif pass_data['devices'][device]['input_output'] == 'Output':
            output_setup(device)
        if pass_data['devices'][device]['reverse_logic'] == 'No':
            if GPIO.input(pass_data['devices'][device]['pin']):
                pass_data['devices'][device]['state'] = 'On' # Set the device state in the live dictionary
            else:
                pass_data['devices'][device]['state'] = 'Off' # Set the device state in the live dictionary
        else:
            if not GPIO.input(pass_data['devices'][device]['pin']):
                pass_data['devices'][device]['state'] = 'On' # Set the device state in the live dictionary
            else:
                pass_data['devices'][device]['state'] = 'Off' # Set the device state in the live dictionary
        if pass_data['devices'][device]['timer_onoff'] == 'On':
            timer_thread_setup(device, pass_data['devices'][device]['pin'])

    
def input_setup(device):
    if (pass_data['devices'][device]['pullup_pulldown'] == 'Pull Up' 
            and pass_data['devices'][device]['input_output'] == 'Input'): # If the device is set to 'Input' and internal resistor 'Pull Up' 
        GPIO.setup(pass_data['devices'][device]['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the pin to input and pull up the pin
    elif (pass_data['devices'][device]['pullup_pulldown'] == 'Pull Down' 
            and pass_data['devices'][device]['input_output'] == 'Input'): # If the device is set to 'Input' and internal resistor 'Pull Down'
        GPIO.setup(pass_data['devices'][device]['pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)# Set the pin to input and pull up the pin

        
def output_setup(device):
    if pass_data['devices'][device]['input_output'] == 'Output': # If the device is set to 'Output'
            GPIO.setup(pass_data['devices'][device]['pin'], GPIO.OUT) # Set the pin to output
    elif (pass_data['devices'][device]['defaultstate'] == 'High' 
            and pass_data['devices'][device]['input_output'] == 'Output'): # If the device is set to 'Output' and the default state is 'High'
        GPIO.output(pass_data['devices'][device]['pin'], GPIO.HIGH) # Set the pin state High
    elif (pass_data['devices'][device]['defaultstate'] == 'Low' 
            and pass_data['devices'][device]['input_output'] == 'Output'): # If the device is set to 'Output' and the default state is 'Low'
        GPIO.output(pass_data['devices'][device]['pin'], GPIO.LOW) # Set the pin state to Low


def timer_thread_setup(device, pin):
    # Device timer thread
    deviceName = device
    device = threading.Thread(target=timer, args=(deviceName, pin))
    device.daemon = True
    device.start()

    
def timer(device, pin):
    while 1:
        if pass_data['devices'][device]['timer_onoff'] == 'On':
            time1 = pass_data['devices'][device]['timeon']
            time2 = pass_data['devices'][device]['timeoff']
            if pass_data['devices'][device]['reverse_logic'] == 'No': # for reverse high/low logic
                GPIO.output(pin, GPIO.HIGH)
                pass_data['devices'][device]['state'] = 'On'
                sleep(float(time1)*3600)
                GPIO.output(pin, GPIO.LOW)
                pass_data['devices'][device]['state'] = 'Off'
                sleep(float(time2)*3600)
            else:
                GPIO.output(pin, GPIO.HIGH)
                pass_data['devices'][device]['state'] = 'Off'
                sleep(float(time1)*3600)
                GPIO.output(pin, GPIO.LOW)
                pass_data['devices'][device]['state'] = 'On'
                sleep(float(time2)*3600)
        else:
            sleep(10)


@app.route('/')
def index():
    return render_template('index.html', pass_data=pass_data)


# For adding new devices    
@app.route('/add', methods=['GET', 'POST'])
def addDevice():
    config.read(configPath)
    if request.method == 'POST':
        request.parameter_storage_class = ImmutableOrderedMultiDict
        lastDevice = request.form['device[]'] # Device Name
        # Form error handling
        if lastDevice == '': # Check is the device name is empty
            flash("Device name can't be empty")
            return redirect(url_for('addDevice'))
        elif lastDevice.lower() == 'default': # Check if the name is 'default' or 'Default'. Configparser doesn't allow sections with that name.
            flash('Device name can\'t be "Default" or "default"')
            return redirect(url_for('addDevice'))
        for device in config.sections()[1:]: # Go through each section minus the first of the config, we just want devices
            if (config.get(device, 'pin') == request.form['pin[]'] 
                    and device == lastDevice): # Check if the device name is taken and if the pin is in use
                flash("Device name already taken and Device pin is already in use.")
                return redirect(url_for('addDevice'))
            elif device == lastDevice: # Check if the name of the device is already in use
                flash("Device name already taken")
                return redirect(url_for('addDevice'))
            elif config.get(device, 'pin') == request.form['pin[]']: # Check if the pin is already in use
                flash("Device pin is already in use.")
                return redirect(url_for('addDevice'))
        else:
            # Add the new device to the config file
            config.add_section(lastDevice)
            config.set(lastDevice, 'pin', request.form['pin[]'])
            config.set(lastDevice, 'input_output', request.form['input_output[]'])
            config.set(lastDevice, 'pullup_pulldown', request.form['pullup_pulldown[]'])
            config.set(lastDevice, 'defaultstate', request.form['high_low[]'])
            config.set(lastDevice, 'timer_onoff', request.form['timer_onoff[]'])
            config.set(lastDevice, 'timer_scale', request.form['timer_scale[]'])
            config.set(lastDevice, 'timeon', request.form['timeon[]'])
            config.set(lastDevice, 'timeoff', request.form['timeoff[]'])
            config.set(lastDevice, 'zone', request.form['zone[]'])
            config.set(lastDevice, 'reverse_logic', request.form['reverse_logic[]'])
            # Add the new device to the live dictionary
            pass_data['devices'][lastDevice] = {}
            pass_data['devices'][lastDevice]['pin'] = request.form['pin[]']
            pass_data['devices'][lastDevice]['input_output'] = request.form['input_output[]']
            pass_data['devices'][lastDevice]['pullup_pulldown'] = request.form['pullup_pulldown[]']
            pass_data['devices'][lastDevice]['defaultstate'] = request.form['high_low[]']
            pass_data['devices'][lastDevice]['timer_onoff'] = request.form['timer_onoff[]']
            pass_data['devices'][lastDevice]['timer_scale'] = request.form['timer_scale[]']
            pass_data['devices'][lastDevice]['timeon'] = request.form['timeon[]']
            pass_data['devices'][lastDevice]['timeoff'] = request.form['timeoff[]']
            pass_data['devices'][lastDevice]['zone'] = request.form['zone[]']
            pass_data['devices'][lastDevice]['reverse_logic'] = request.form['reverse_logic[]']
            pass_data['devices'][lastDevice]['state'] == 'Off'
            if pass_data['devices'][lastDevice]['timer_onoff'] == 'On':
                timer_thread_setup(lastDevice, pass_data['devices'][lastDevice]['pin'])
            # Write the new configs to the config file
            with open(configPath, "wb") as config_file:
                config.write(config_file)
    return render_template('addDevice.html', pass_data=pass_data)


# For editing device settings
@app.route('/edit', methods=['GET', 'POST'])
def editDevice():
    config.read(configPath)
    if request.method == 'POST':
        if request.form['submit'] == 'Update Device Settings': # If request is Update Device Settings
            request.parameter_storage_class = ImmutableOrderedMultiDict
            device = request.form['device[]']
            # Remove all current options from the device in the config
            config.remove_option(device, 'pin')
            config.remove_option(device, 'input_output')
            config.remove_option(device, 'pullup_pulldown')
            config.remove_option(device, 'defaultstate')
            config.remove_option(device, 'timer_onoff')
            config.remove_option(device, 'timer_scale')
            config.remove_option(device, 'timeon')
            config.remove_option(device, 'timeoff')
            config.remove_option(device, 'zone')
            config.remove_option(device, 'reverse_logic')
            # Set the new option settings for the device in the config
            config.set(device, 'pin', request.form['pin[]'])
            config.set(device, 'input_output', request.form['input_output[]'])
            config.set(device, 'pullup_pulldown', request.form['pullup_pulldown[]'])
            config.set(device, 'defaultstate', request.form['high_low[]'])
            config.set(device, 'timer_onoff', request.form['timer_onoff[]'])
            config.set(device, 'timer_scale', request.form['timer_scale[]'])
            config.set(device, 'timeon', request.form['timeon[]'])
            config.set(device, 'timeoff', request.form['timeoff[]'])
            config.set(device, 'zone', request.form['zone[]'])
            config.set(device, 'reverse_logic', request.form['reverse_logic[]'])
            # Update the live dictionary with the new settings
            pass_data['devices'][device]['pin'] = request.form['pin[]']
            pass_data['devices'][device]['input_output'] = request.form['input_output[]']
            pass_data['devices'][device]['pullup_pulldown'] = request.form['pullup_pulldown[]']
            pass_data['devices'][device]['defaultstate'] = request.form['high_low[]']
            pass_data['devices'][device]['timer_onoff'] = request.form['timer_onoff[]']
            pass_data['devices'][device]['timer_scale'] = request.form['timer_scale[]']
            pass_data['devices'][device]['timeon'] = request.form['timeon[]']
            pass_data['devices'][device]['timeoff'] = request.form['timeoff[]']
            pass_data['devices'][device]['zone'] = request.form['zone[]']
            pass_data['devices'][device]['reverse_logic'] = request.form['reverse_logic[]']
            with open(configPath, "wb") as config_file: # Write the new configs to the config file
                config.write(config_file)
        if request.form['submit'] == 'Remove Device': # If request is to remove device
            config.remove_section(request.form['device[]']) # Remove the device from the config
            pass_data['devices'].pop(request.form['device[]'], None) # Remove the device from the live dictionary
            with open(configPath, "wb") as config_file: # Write the new configs to the config file
                config.write(config_file)
    return redirect(url_for('addDevice'))


# For editing the global zone count    
@app.route('/zoneCount', methods=['POST'])
def zoneCount():
    config.read(configPath)
    zone_count = request.form['zone[]']
    config.set('zones', 'zone_count', zone_count)
    with open(configPath, "wb") as config_file:
        config.write(config_file)
    return redirect(url_for('addDevice'))


# ajax GET call function to set state of pins
@app.route("/_state")
def _state():
    state = request.args.get('state') # Get the current state of the button from the web page
    pin = request.args.get('pin') # Get the current pin from the web page
    pin = pin.split(':')
    print(pin)
    if pass_data['devices'][pin[0]]['reverse_logic'] == 'No': # for reverse high/low logic
        if state=="Power On": # If the current state of the button is 'Power On'
            GPIO.output(pin[1], GPIO.HIGH) # Set that pin state to High
        else:
            GPIO.output(pin[1], GPIO.LOW) # Set the pin state to Low
        for device in pass_data['devices']: # Go through devices and set their current state in the live dictionary
            if GPIO.input(pass_data['devices'][device]['pin']):
                pass_data['devices'][device]['state'] = 'On' # Set the device state in the live dictionary
            else:
                pass_data['devices'][device]['state'] = 'Off' # Set the device state in the live dictionary
    else: # for reverse high/low logic
        if state=="Power On": # If the current state of the button is 'Power On'
            GPIO.output(pin[1], GPIO.LOW) # Set that pin state to Low
        else:
            GPIO.output(pin[1], GPIO.HIGH) # Set the pin state to High
        for device in pass_data['devices']: # Go through devices and set their current state in the live dictionary
            if not GPIO.input(pass_data['devices'][device]['pin']):
                pass_data['devices'][device]['state'] = 'On' # Set the device state in the live dictionary
            else:
                pass_data['devices'][device]['state'] = 'Off' # Set the device state in the live dictionary
    return ""


def event_stream():
    while True:
        gevent.sleep(1)
        for device in pass_data['devices']:
            pin = pass_data['devices'][device]['pin']
            if pass_data['devices'][device]['state'] == 'On':
                print('data: %s %s Power On \n\n' % (device, pin))
                yield 'data: %s %s Power On \n\n' % (device, pin)
            else:
                print('data: %s %s Power Off \n\n' % (device, pin))
                yield 'data: %s %s Power Off \n\n' % (device, pin)


@app.route('/my_event_source')
def sse_request():
    return Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    get_devices()
    #app.debug = True
    #app.run('0.0.0.0', 5000)
    print('Starting web server')
    server = WSGIServer(('0.0.0.0', 5000), app)
    print('Web server running..')
    server.serve_forever()
