#Obselete code - GUI is now integrated into Client.py

import tkinter as tk
import Get_Functions as gf

window = tk.Tk()
window.title("Chatbot Jeff")
window.geometry("300x300")
window.configure(background="cornflower blue")

lblTitle = tk.Label(window, text="CHATBOT JEFF\n\n", bg="cornflower blue", font=(24))
lblTitle.pack()

userInput = tk.Entry(window)
userInput.pack()

lbl = tk.Label(window, text="\nChatHistory", bg="cornflower blue")
lbl.pack()

def cb(event): #Richard
    userText = userInput.get()
    userName = gf.getName(userText)
    userName = userName.title()
    botText = "Hello " + userName + ", it's nice to meet you"
    msgBox.configure(state="normal")
    msgBox.insert(tk.END, "User: " + userText + "\n")
    msgBox.insert(tk.END, "Bot: " + botText + "\n")
    msgBox.configure(state="disabled")

userInput.bind("<Return>", cb)
msgBox = tk.Text(window)
msgBox.pack()

tk.mainloop()
