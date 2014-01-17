# import GPIO library
import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set pin 18 to output mode
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.IN)

print 'lets get started'
while True:
    if (GPIO.input(22) == False):
        print 'button pushed'
        execfile('blinking_leds.py')
    else:
        GPIO.output(18, GPIO.LOW)
