#키보드 1또는 2를 입력받아 이미지를 다르게 띄우는 프로그
from tkinter import *

from PIL import Image, ImageTk

root = Tk()  # A root window for displaying objects
# open image
imageHead = Image.open('gauge.png')
imageHand = Image.open('snow.png')
imageHead_original = Image.open('gauge.png')

imageHand=imageHand.resize((150, 150), Image.ANTIALIAS)

imageHead.paste(imageHand, (430, 220), imageHand)
# Convert the Image object into a TkPhoto object
tkimage = ImageTk.PhotoImage(imageHead)
tkimage2 = ImageTk.PhotoImage(imageHead_original)

data = 1

def poll():
    global data
    print("hello")
    data = input()
    data =int(data)
    print(data)
    if data == 1:
        panel1 = Label(root, image=tkimage)
        panel1.grid(row=3, column=3, sticky=E)
        root.after(10, poll)

    elif data == 2:
        panel1 = Label(root, image=tkimage2)
        panel1.grid(row=3, column=3, sticky=E)
        root.after(10, poll)


    
root.after(10, poll)
root.mainloop()
        
        


        
    
    
    
