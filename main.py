from flask import Flask, render_template, request, redirect, url_for, flash
from ConfigParser import SafeConfigParser
from werkzeug.datastructures import ImmutableOrderedMultiDict

app = Flask(__name__)
app.secret_key = "super secret key"
# Load the config file
config = SafeConfigParser()
configPath = 'usersettings.ini'

chip_io = ['TWI1-SDA', 'TWI1-SCK', 'LCD-D2', 'PWM0', 'LCD-D4', 'LCD-D3', 'LCD-D6', 'LCD-D5', 
            'LCD-D10', 'LCD-D7', 'LCD-D12', 'LCD-D11', 'LCD-D14', 'LCD-D13', 'LCD-D18', 
            'LCD-D15', 'LCD-D20', 'LCD-D19', 'LCD-D22', 'LCD-D21', 'LCD-CLK', 'LCD-D23', 
            'LCD-VSYNC', 'LCD-HSYNC', 'LCD-DE', 'UART1-TX', 'UART1-RX', 'LRADC', 'XIO-P0', 
            'XIO-P1', 'XIO-P2', 'XIO-P3', 'XIO-P4', 'XIO-P5', 'XIO-P6', 'XIO-P7', 'AP-EINT1', 
            'AP-EINT3', 'TWI2-SDA', 'TWI2-SCK', 'CSIPCK', 'CSICK', 'CSIHSYNC', 'CSIVSYNC', 
            'CSID0', 'CSID1', 'CSID2', 'CSID3', 'CSID4', 'CSID5', 'CSID6', 'CSID7']

@app.route('/')
def index():
    config.read(configPath)
    zones = config.get('zones', 'zone_count')
    pass_data = []
    pass_data.append(chip_io)
    for device in config.sections()[1:]:
        deviceData = []
        for deviceOptions in config.options(device):
            deviceData.append(config.get(device, deviceOptions))
        pass_data.append((device, deviceData))
    pass_data.append(int(zones))
    return render_template('index.html', pass_data=pass_data)
    
@app.route('/add', methods=['GET', 'POST'])
def addDevice():
    config.read(configPath)
    zones = config.get('zones', 'zone_count')
    pass_data = []
    pass_data.append(chip_io)
    if request.method == 'POST':
        request.parameter_storage_class = ImmutableOrderedMultiDict
        lastDevice = request.form['device[]']
        if lastDevice == '':
            flash("Device name can't be empty")
            return redirect(url_for('addDevice'))
        elif lastDevice.lower() == 'default':
            flash('Device name can\'t be "Default" or "default"')
            return redirect(url_for('addDevice'))
        for device in config.sections()[1:]:
            if config.get(device, 'pin') == request.form['pin[]'] and device == lastDevice:
                flash("Device name already taken and Device pin is already in use.")
                return redirect(url_for('addDevice'))
            elif device == lastDevice:
                flash("Device name already taken")
                return redirect(url_for('addDevice'))
            elif config.get(device, 'pin') == request.form['pin[]']:
                flash("Device pin is already in use.")
                return redirect(url_for('addDevice'))
        else:
            config.add_section(lastDevice)
            config.set(lastDevice, 'pin', request.form['pin[]'])
            config.set(lastDevice, 'input_ouput', request.form['input_output[]'])
            config.set(lastDevice, 'pullup_pulldown', request.form['pullup_pulldown[]'])
            config.set(lastDevice, 'defaultstate', request.form['high_low[]'])
            config.set(lastDevice, 'zone', request.form['zone[]'])
            with open(configPath, "wb") as config_file:
                config.write(config_file)
    for device in config.sections()[1:]:
        deviceData = []
        for deviceOptions in config.options(device):
            deviceData.append(config.get(device, deviceOptions))
        pass_data.append((device, deviceData))
    pass_data.append(int(zones))
    return render_template('addDevice.html', pass_data=pass_data)
    
@app.route('/edit', methods=['GET', 'POST'])
def editDevice():
    config.read(configPath)
    pass_data = []
    pass_data.append(chip_io)
    if request.method == 'POST':
        if request.form['submit'] == 'Update Device Settings':
            request.parameter_storage_class = ImmutableOrderedMultiDict
            device = request.form['device[]']
            config.remove_option(device, 'pin')
            config.remove_option(device, 'input_ouput')
            config.remove_option(device, 'pullup_pulldown')
            config.remove_option(device, 'defaultstate')
            config.remove_option(device, 'zone')
            config.set(device, 'pin', request.form['pin[]'])
            config.set(device, 'input_ouput', request.form['input_output[]'])
            config.set(device, 'pullup_pulldown', request.form['pullup_pulldown[]'])
            config.set(device, 'defaultstate', request.form['high_low[]'])
            config.set(device, 'zone', request.form['zone[]'])
            with open(configPath, "wb") as config_file:
                config.write(config_file)
        if request.form['submit'] == 'Remove':
            config.remove_section(request.form['device[]'])
            with open(configPath, "wb") as config_file:
                config.write(config_file)
    return redirect(url_for('addDevice'))
    
@app.route('/zoneCount', methods=['POST'])
def zoneCount():
    config.read(configPath)
    zone_count = request.form['zone[]']
    config.set('zones', 'zone_count', zone_count)
    with open(configPath, "wb") as config_file:
        config.write(config_file)
    return redirect(url_for('addDevice'))

if __name__ == '__main__':
    app.debug = True
    app.run()