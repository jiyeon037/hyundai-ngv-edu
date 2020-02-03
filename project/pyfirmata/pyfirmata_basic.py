from pyfirmata import Arduino, util 
import time 

port = 'COM21' 
BUTTON = 8 
LED_RED = 13 

board = Arduino(port) 
time.sleep(1) 

board.get_pin('d:8:i') 
board.get_pin('d:13:o') 

iterater = util.Iterator(board) 
iterater.start() 
print("Interater starts.") 

while(True): 
   button = board.digital[BUTTON].read() 
   if(button == True): 
       print("button pressed.") 
       board.digital[LED_RED].write(1) 
       time.sleep(0.5) 
       board.digital[LED_RED].write(0) 
       time.sleep(0.5) 
       print(button) 
   elif(button == False): 
       board.digital[LED_RED].write(0) 
       time.sleep(0.5) 
       print(button) 
board.exit()
