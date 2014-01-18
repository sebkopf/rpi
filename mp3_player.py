# import GPIO library
import RPi.GPIO as GPIO
import time as time
import os # to be able to run commands

#set audio output to analog
os.system('amixer cset numid=3 1')

# set upt GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set pin 18 (LED) to output mode and define functions to turn it on/off
GPIO.setup(18, GPIO.OUT)
led_status = False
def led_off(pin=18):
    GPIO.output(pin, GPIO.LOW)
def led_on(pin=18):
    GPIO.output(pin, GPIO.HIGH)

# set input (button) pins
GPIO.setup(22, GPIO.IN)

print 'lets get started'
led_off()
while True:
    if (GPIO.input(22) == False):
        if (led_status == False):
            print 'button pushed'
            led_status = True
            led_on()
            os.system('mpg123 -vC class.mp3')
        else:
            print 'button pushed again'
            led_status = False
            led_off()
            time.sleep(1)
