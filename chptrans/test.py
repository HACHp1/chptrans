from tkinter import *
import time
 
num=0
 
tk=Tk()
canvas=Canvas(tk,width=500,height=500)
canvas.pack()
itext=canvas.create_text(30,30,text=str(num))
while num<7:
    num +=1
    canvas.itemconfig(itext,text=str(num))
    canvas.insert(itext,12,'')
    tk.update()
    print('num=%d'%num)
    tk.after(1000)