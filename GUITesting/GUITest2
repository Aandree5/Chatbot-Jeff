import random
import tkinter as tk
import Get_Functions as GF

root = tk.Tk()
root.geometry("150x150")

lblNameAsk = tk.Label(root, text="What is your name?")
lblNameAsk.pack()

userInput = tk.Entry(root)
userInput.pack()

def cb(event):
    userText = userInput.get()
    userName = GF.getName(userText)
    userName = userName.title()
    botText = "Hello " + userName + ", it's nice to meet you"
    output.config(text=botText)

userInput.bind("<Return>", cb)
output = tk.Label(root, text='')
output.pack()

tk.mainloop()
