#!/usr/bin/python
 
import RPi.GPIO as GPIO
import pigpio
import time
import sys
import os
import signal
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
tilt = 4
br = 21
bl = 6
trig = 23
echo = 24
head = 26
 
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
 
pi = pigpio.pi()
 
 
def backward():
    pi.set_servo_pulsewidth(tilt, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 800)    
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 2000)
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 1500) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1500)   
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1500)   
    time.sleep(0.15)
    return;
 
def forward():
    pi.set_servo_pulsewidth(tilt, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1800)       
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 2000)
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 1500) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1500)   
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1500)   
    time.sleep(0.15)
    return;
 
def left():
    pi.set_servo_pulsewidth(tilt, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1800)       
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 2000)
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 1500) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1500)   
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1500)   
    time.sleep(0.15)
    return;
 
def right():
    pi.set_servo_pulsewidth(tilt, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 800)    
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 2000)
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 800) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(tilt, 1500) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 1500)   
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 1500)   
    time.sleep(0.15)
    return;
     
def stop():
    pi.set_servo_pulsewidth(tilt, 0) 
    time.sleep(0.15)
    pi.set_servo_pulsewidth(bl, 0)   
    time.sleep(0.15)
    pi.set_servo_pulsewidth(br, 0)   
    time.sleep(0.15)
     
    return
 
def obstacleDetected():
    backward()
    backward()
    backward()
    backward()
    backward()
    right()
    right()
    right()
     
    return
 
def turnHead():
    pi.set_servo_pulsewidth(head, 700)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(head, 2100)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(head, 1500)
    time.sleep(0.5)
 
    return
 
def autoMode():
    print ("Running in auto mode!")
 
    turnHead()
     
    time.sleep(0.5)
    GPIO.output(trig, 0)
    time.sleep(0.5)
     
    GPIO.output(trig,1)
    time.sleep(0.00001)
    GPIO.output(trig,0)
     
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
     
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
 
    pulse_duration = pulse_end - pulse_start
     
    distance = pulse_duration * 17150
     
    distance = round(distance, 2)
     
    if distance > 1 and distance < 35:
        obstacleDetected()
    else:
        forward()
        forward()
        forward()
     
    pi.set_servo_pulsewidth(head, 2100)
    time.sleep(0.5)
    return
     
def manualMode():
    move = str(sys.argv[2])
    if move == "F" or move == "f":
        print("Moving forward!")
        forward()
    elif move == "B" or move == "b":
        print("Moving backward!")
        backward()
    elif move == "L" or move == "l":
        print("Moving left!")
        left()
    elif move == "R" or move == "r":
        print("Moving right!")
        right()
    else:
        print("Invalid argument!")
     
    return
     
def main():
    opt = str(sys.argv[1])
     
    if opt == "A" or opt == "a":
        autoMode()
    elif opt == "M" or opt == "m":
        manualMode()
     
    return
         
while True:
    main()
 
GPIO.cleanup()
pi.stop()