
from pyfirmata import Arduino, util 
import time 

port = 'COM23' 
BUTTON = 2 
LED_RED = 13 

H_R=10 
H_G=9 
H_B=11 
L_R=6 
L_G=5 
L_B=4 

board = Arduino(port) 
time.sleep(1) 

board.get_pin('d:2:i') 

board.get_pin('d:4:o') 
board.get_pin('d:5:o') 
board.get_pin('d:6:o') 
board.get_pin('d:9:o') 
board.get_pin('d:10:o') 
board.get_pin('d:11:o') 

board.get_pin('d:13:o') 

iterater = util.Iterator(board) 
iterater.start() 
def ALLOF(): 
   board.digital[H_R].write(0) 
   board.digital[H_G].write(0) 
   board.digital[H_B].write(0) 
   board.digital[L_R].write(0) 
   board.digital[L_G].write(0) 
   board.digital[L_B].write(0) 

def ROAD_RED(): 
   board.digital[H_R].write(0) 
   board.digital[H_G].write(0) 
   board.digital[H_B].write(1) 
   board.digital[L_R].write(1) 
   board.digital[L_G].write(0) 
   board.digital[L_B].write(0) 

def ROAD_YELLOW(): 
   board.digital[H_R].write(1) 
   board.digital[H_G].write(0) 
   board.digital[H_B].write(0) 
   board.digital[L_R].write(1) 
   board.digital[L_G].write(1) 
   board.digital[L_B].write(0) 
    
def ROAD_BLUE(): 
   board.digital[H_R].write(0) 
   board.digital[H_G].write(0) 
   board.digital[H_B].write(1) 
   board.digital[L_R].write(1) 
   board.digital[L_G].write(0) 
   board.digital[L_B].write(0) 
    
while(True): 
   button = board.digital[BUTTON].read() 
   print(button) 
   if(button == False): 
       board.digital[H_R].write(1) 
       board.digital[L_G].write(1) 
       board.digital[L_R].write(1) 
       time.sleep(5) 
       ALLOF(); 
        
       board.digital[H_B].write(1) 
       board.digital[L_R].write(1) 
       time.sleep(5) 
       ALLOF(); 
        
       for i in range(10): 
           board.digital[H_B].write(1) 
           board.digital[L_R].write(1) 
           time.sleep(1) 
           board.digital[H_B].write(0) 
           time.sleep(1) 

   if(button == True): 
       ROAD_BLUE() 
       time.sleep(5) 
       ROAD_YELLOW() 
       time.sleep(5) 
       ROAD_RED() 
       time.sleep(5) 
board.exit() 

