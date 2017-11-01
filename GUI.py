import tkinter #imports the tkinter GUI framework
import Get_Functions #imports the Get_Functions.py file so that the GUI can access the chatbot text recognition functions

window = tkinter.Tk() #creates an object called window, this is the main window which all the GUI elements are displayed in

#configures the window so it displays correctly
window.title("Chatbot Jeff")
window.geometry("600x800")
window.configure(background="cornflower blue")

#creates title text displayed in the window
lblTitle = tkinter.Label(window, text="CHATBOT JEFF\n\n", bg="cornflower blue", font=(24))
lblTitle.grid(row = 0, column = 1)

#creates intro text
lblDesc = tkinter.Label(window, text="Welcome to Chatbot-Jeff\n\nThis chatbot was created by ALL group A1\n\n\n", bg="cornflower blue")
lblDesc.grid(row = 2, column = 1)

#creates the button (currently a non-functional button)
btnBegin = tkinter.Button(window, text="Click To Launch Chatbot")
btnBegin.grid(row = 3, column = 1)

def fetchFunc():
    usrInput = entry.get()
    lblUsrIn = tkinter.Label(window, text=usrInput)
    lblUsrIn.grid(row = 6, column = 2)
    return 0

entry = tkinter.Entry(window)
entry.grid(row = 5, column = 1)
btnSubmit = tkinter.Button(window, text="Submit", command=fetchFunc)
btnSubmit.grid(row = 6, column = 1)

window.mainloop()
