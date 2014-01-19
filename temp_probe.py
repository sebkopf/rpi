import os # for issuing os commands
import glob # for reading file structure
import time # for keeping time
import RPi.GPIO as GPIO #interacting with the GPIO

print 'Welcome to the temperature probe test'

# set upt GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set up LEDs
LEDs = {'red':18, 'green':17, 'yellow':23}
for col in LEDs:
    print 'Setting up', col, 'LED - GPIO PIN', LEDs[col]
    GPIO.setup(LEDs[col], GPIO.OUT)
def led_status(cols, signal):
    if isinstance(cols, str): # only a single color
        GPIO.output(LEDs[cols], signal)
    else: # multiple colors
        for col in cols:
            GPIO.output(LEDs[col], signal)
def led_off(cols): led_status(cols, GPIO.LOW)
def led_on(cols): led_status(cols, GPIO.HIGH)
led_off(LEDs.keys())

# start temperature probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# access probe readout
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
if len(device_folders) > 0:
    # just pick first probe (FIXME: in case there are more than one)
    device_file = device_folders[0] + '/w1_slave'
else:
    print '\n\tERROR: could not find an active temperature device in', base_dir, '\n'
    print 'Exiting program.'
    exit()

# read temperature from file
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# display temperature reading
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES': # check if there is a reported temp
        print 'No temperature reported, trying again...'
        led_on('red')
        time.sleep(0.2)
        led_off('red')
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1: # found a temperature reading
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# time variables
READ = 1.0 # [s] how often to read temp

# main loop
print 'Reading temperature every', READ, 'seconds'
temp_c_prev = 0.
while True:
    led_on('green')
    [temp_c, temp_f]= read_temp() # reading temperature
    led_off('green')
    if temp_c > temp_c_prev:
        led_on('red')
        temp_c_prev = temp_c
        print 'Temperature increased to', temp_c, 'C (', temp_f, 'F)'
        time.sleep(READ)
        led_off('red')
    elif temp_c < temp_c_prev:
        led_on('yellow')
        temp_c_prev = temp_c
        print 'Temperature decreased to', temp_c, 'C (', temp_f, 'F)'
        time.sleep(READ)
        led_off('yellow')
    else:
        time.sleep(READ)

