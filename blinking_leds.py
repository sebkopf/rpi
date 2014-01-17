# import GPIO library
import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)
# set pin 18 to output mode
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

def blink(pins, interval=0.03):
    leds_on(pins)
    time.sleep(interval)
    leds_off(pins)
    time.sleep(interval)

def leds_off(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

def leds_on(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
    
i = 0
while i < 100:
    i = i + 1
    if i % 10 == 0:
        blink([17, 18, 23])
    elif i % 5 == 0:
        blink([17, 23])
    else:
        blink([17])


leds_off([17, 18, 23])
