##################################################################
##  The primary code which will be run by a deamon on the rPI	##
##  OWL v2.1							##
##  Srujana Center for Innovation, LV Prasad Eye Institute	##
##  								##
##  This code will wait for an external button press, capture	##
##  two images in rapid succession with two different white  	##
##  LEDs, process them to remove glare computationally, send	##
##  them to the theia algo backend to be processed, save them	##
##  and return the score on-screen in human readable format.	##
##								##
##################################################################

import time
import picamera
import RPi.GPIO as GPIO

# set the pins
white = 14
# ^^^this pin is active LOW, hence note the True and False being counterintuitive
IR = 15
switch = 18
i=1

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(white,GPIO.OUT)
GPIO.setup(IR, GPIO.OUT)

# setting white ON but IR off
GPIO.output(white, False)
GPIO.output(IR, True)

with picamera.PiCamera() as camera:
    camera.resolution = (2592,1944);
    try:
        while True:
             filename = 'images/image',i,'.jpg'
             camera.start_preview()
            # GPIO.output(IR, True)
             GPIO.wait_for_edge(switch,GPIO.RISING)
            
	    # The following stuff happens when the buton is pressed
             GPIO.output(IR, True)
             GPIO.output(white, False)
             camera.capture('images/image'+str(i)+'.jpg',use_video_port=True)
	    #Set the white LED OFF
             GPIO.output(white, False)
             GPIO.output(IR, True)
             camera.stop_preview()
             i=i+1
    except  KeyboardInterrupt: 
    #    except ValueError:
    
        print "Interrupted"
        GPIO.output(white, True)
        GPIO.output(IR, True)
        GPIO.cleanup()
