# -*- coding: utf-8 -*-
# add servo pwm generator
# joy stick dependency
# 아직 테스트 이전 소스

import time
import pygame
import RPi.GPIO as GPIO

# pca9685 pwm dependency
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Settings for joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 3                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped

global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
pwm.set_pwm_freq(60) # 서보모터(SG90)에 최적화된 69Hz로 펄스주기를 설정.

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight

    #조이스틱 이벤트 발생한 경우
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            if upDown < -0.1:
                moveUp = True
                moveDown = False
            elif upDown > 0.1:
                moveUp = False
                moveDown = True
            else:
                moveUp = False
                moveDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                moveLeft = True
                moveRight = False
            elif leftRight > 0.1:
                moveLeft = False
                moveRight = True
            else:
                moveLeft = False
                moveRight = False
try:
    print ('Press [ESC] or Press PS3 O button to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            hadEvent = False
            if moveLeft:
                print("LEFT")
                pwm.set_pwm(3, 0, 170) #1번서보를 펄스길이(170)으로 설정.
            if moveRight:
                print("RIGHT")
                pwm.set_pwm(3, 0, 400) #1번서보를 펄스길이(400)으로 설정.
                
            if moveUp:
                print("GO")
                pwm.set_pwm(0, 0, 170)
            if moveDown:
                print("BACK")
                pwm.set_pwm(0, 0, 400)
                
            if moveUp == False and moveDown == False :
                pwm.set_pwm(0, 0, 285)
            if moveLeft == False and moveRight == False :
                pwm.set_pwm(3, 0, 285)
                
except KeyboardInterrupt:
    print("EMERGENCY STOP")
