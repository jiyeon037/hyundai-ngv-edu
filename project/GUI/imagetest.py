#키보드 1 또는 2를 입력받아 이미지를 다르게 띄우는 프로그램
# GUI 툴이 프로세스를 많이 잡아먹는거를 수정해야될 듯.....
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

panel1 = Label(root, image=tkimage)
panel1.grid(row=3, column=3, sticky=E)

def poll():
    global data
    print(data)
    if data == 1:
        print("img1")
        panel1 = Label(root, image=tkimage)
        panel1.grid(row=3, column=3, sticky=E)
        data= 3
        root.after(1, LOOP)

    elif data == 2:
        print("img2")
        panel1 = Label(root, image=tkimage2)
        panel1.grid(row=3, column=3, sticky=E)
        data= 3
        root.after(1, LOOP)
        
        
    else:
        root.after(1, LOOP)

        
def LOOP():
    if True:
        print("LOOP");
        global data
        data = int(input())
        print(data)
        if(data == 1 or data == 2):
            print("goto poll")
            root.after(1, poll)

    ## loop문 시작
        print("WAIT")
    

    
    ## loop문 끝
    
root.after(1000, LOOP)
root.mainloop()
        
        


        
    
    
    
