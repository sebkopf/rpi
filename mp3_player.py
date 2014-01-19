# import GPIO library
import RPi.GPIO as GPIO #interacting with the GPIO
import time as time # keeping track of time
import glob # reading file system
import os # to be able to run command line commands
#from subprocess import Popen, PIPE, STDOUT # running e.g. an os process as subprocess
import pygame # for playing music from python

print 'Welcome to the MP3 player'

#set audio output to analog
#os.system('amixer cset numid=3 1')

# set upt GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set LED pins to output mode and define functions to turn them on/off
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
LED_red = 18
LED_green = 17
LED_yellow = 23
LED_all = [LED_red, LED_green, LED_yellow]
def led_off(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
def led_on(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
led_off(LED_all)

# set input (button) pins
GPIO.setup(22, GPIO.IN)
GPIO.setup(25, GPIO.IN)

# fetch mp3 files
mFiles = glob.glob("*.mp3")
nMusic = len(mFiles)
iMusic = -1

# constants
QUIT = 1 # seconds to press button 1
BLINK = 0.5 # seconds for leds to blink
FFORWARD = 0.5 # seconds for fast forward to kick in (and interval between skips)
SKIP = 1 # seconds to skip

# status variables
button1_pushed = False
button1_time = 0
button2_pushed = False
button2_time = 0
start_pos = 0 # starting position of file in seconds
playing = False
fforwarding = False
blinking_time = time.clock()
blinking_status = False
blinking_LEDs = []

# functions to control playing
def song_load():
    global iMusic
    iMusic = (iMusic + 1) % nMusic
    print 'Loading', mFiles[iMusic], '...'
    pygame.mixer.music.load(mFiles[iMusic])
    pygame.mixer.music.play()
    pygame.mixer.music.pause() 

def song_play():
    global playing, blinking_LEDs
    print 'Playing'
    pygame.mixer.music.unpause()
    playing = True
    blinking_LEDs = []
    led_on([LED_green]) # during playing, green LED is on 

def song_pause():
    global playing, blinking_LEDs
    print 'Pausing...'
    pygame.mixer.music.pause()
    playing = False
    blinking_LEDs = [LED_green]# during pause, blink green LED
     
def song_ff():
    global fforwarding, blinking_LEDs, start_pos
    if (playing == False):
        song_play() # need to be playing a song to fast forward
    if (fforwarding == False):
        print 'Fast forwarding...' # show message only once
    fforwarding = True
    start_pos = start_pos + pygame.mixer.music.get_pos()/1000. + SKIP
    pygame.mixer.music.play(0, start_pos) #FIXME: this is a workaround set_pos is not supported!
    blinking_LEDs = [LED_yellow]

def song_next():
    global start_pos
    print 'Skipping to next track'
    start_pos = 0
    song_load()
    song_play()
    
# initialize pygame
print 'Initializing audio...'
pygame.mixer.init()
song_load()

# main listening loop
print 'Ready to go!'
while True:
    # LED blinking
    if ((time.clock() - blinking_time) > BLINK):
        blinking_time = time.clock()
        if (blinking_status == False):
            led_on(blinking_LEDs)
            blinking_status = True
        else:
            led_off(blinking_LEDs)
            blinking_status = False
    # next button
    if (GPIO.input(25) == False): # button pressed
        if (button2_pushed == False):
            button2_pushed = True
            led_on([LED_yellow])
            button2_time = time.clock() # start timer for fast forward
        elif (button2_pushed == True and (time.clock() - button2_time) > FFORWARD): # time to ffowrard
            song_ff()
            button2_time = time.clock()
    else: # button released
        if (button2_pushed == True):
            button2_pushed = False
            led_off([LED_yellow])
            if (fforwarding == True):
                fforwarding = False
                song_play()
            else:
                song_next()
    # start /stop button
    if (GPIO.input(22) == False): # button pressed
        if (button1_pushed == False):
            button1_pushed = True
            button1_time = time.clock() # start timer for program quit
        elif (button1_pushed == True and (time.clock() - button1_time) > QUIT): # time to quit # time to quit
            led_off(LED_all)
            led_on([LED_red])
            break
    else: # button released, start action
        if (button1_pushed == True):
            button1_pushed = False
            led_off(LED_all)
            if (playing == True): song_pause()
            elif (playing == False):song_play()

 
# shutting everything down
print 'Turning off MP3 player.'
pygame.mixer.music.fadeout(3000)
time.sleep(3)
led_off(LED_all)
print 'Good bye.'

