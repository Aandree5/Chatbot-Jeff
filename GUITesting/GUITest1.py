import random
import tkinter as tk

root = tk.Tk()
userInput = tk.Entry(root)
userInput.pack()

greetings = ['hola', 'hello', 'hi', 'hey!', 'hey']
question = ['how are you?', 'how are you doing?', 'how are you', 'how are you doing']
responses = ['Okay', "I'm fine"]
huh = "I did not understand what you said"

def cb(event):
    userText = userInput.get()
    userText = userText.lower()
    if userText in greetings:
        botText = random.choice(greetings)
    elif userText in question:
        botText = random.choice(responses)
    else:
        botText = huh
    output.config(text=botText)

userInput.bind("<Return>", cb)
output = tk.Label(root, text='')
output.pack()

tk.mainloop()
