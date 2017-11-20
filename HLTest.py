#Obselete Code - Used to test external code stored in tkHyperlinkManager.py

import tkHyperlinkManager
import webbrowser
import tkinter as tk

root = tk.Tk()
root.title("Hyperlink Manager Test")

text = tk.Text(root)
text.pack()

hyperlink = tkHyperlinkManager.HyperlinkManager(text)

def click1(): #Richard
    print ("click 1")
    url = "https://www.google.co.uk"
    webbrowser.open(url, new=2)

text.insert(tk.INSERT, "this is a ")
text.insert(tk.INSERT, "link", hyperlink.add(click1))
text.insert(tk.INSERT, "\n\n")

def click2(): #Richard
    print ("click 2")
    url = "https://www.google.co.uk"
    webbrowser.open(url, new=2)

text.insert(tk.INSERT, "this is another ")
text.insert(tk.INSERT, "link", hyperlink.add(click2))
text.insert(tk.INSERT, "\n\n")

tk.mainloop()
