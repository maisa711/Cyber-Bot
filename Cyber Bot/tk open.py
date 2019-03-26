import sys
import os
from tkinter import *

window=Tk()

window.title("SCSA Robot")
window.geometry('500x171')

def run():
    os.system('robotv.py')
def run2():
    os.system('robott.py')

btn = Button(window, text="Voice Input", bg="black", fg="white",command=run, width=40, height=3)
btn2 = Button(window, text="Text Input", bg="black", fg="white",command=run2, width=40, height=3)
btn3 = Button(window, text="Quit", bg="white", fg="black",command=quit, width=30, height=3)

btn.pack()
btn2.pack()
btn3.pack()
window.mainloop()

