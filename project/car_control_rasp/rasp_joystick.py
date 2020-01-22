# -*- coding: utf-8 -*-
import time
import pygame
import RPi.GPIO as GPIO

def MotorOff():
    print("MOTOR OFF")

# Settings for JoyBorg
leftDrive = DRIVE_1                     # Drive number for left motor
rightDrive = DRIVE_4                    # Drive number for right motor
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
            elif moveRight:
                print("RIGHT")
            elif moveUp:
                print("GO")
            elif moveDown:
                print("BACK")
            else:
                print("STOP")
            
except KeyboardInterrupt:
    print("EMERGENCY STOP")
