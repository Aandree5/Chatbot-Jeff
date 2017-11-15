import tkHyperlinkManager
import webbrowser
from tkinter import *

root = Tk()
root.title("hyperlink-1")

text = Text(root)
text.pack()

hyperlink = tkHyperlinkManager.HyperlinkManager(text)

def click1():
    print ("click 1")
    url = "https://www.google.co.uk"
    webbrowser.open(url, new=2)

text.insert(INSERT, "this is a ")
text.insert(INSERT, "link", hyperlink.add(click1))
text.insert(INSERT, "\n\n")

def click2():
    print ("click 2")

text.insert(INSERT, "this is another ")
text.insert(INSERT, "link", hyperlink.add(click2))
text.insert(INSERT, "\n\n")

mainloop()
