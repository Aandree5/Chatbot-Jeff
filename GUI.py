import tkinter #imports the tkinter GUI framework
import Get_Functions #imports the Get_Functions.py file so that the GUI can access the chatbot text recognition functions

window = tkinter.Tk() #creates an object called window, this is the main window which all the GUI elements are displayed in

#configures the window so it displays correctly
window.title("Chatbot Jeff")
window.geometry("600x800")
window.configure(background="cornflower blue")

#creates title text displayed in the window
lblTitle = tkinter.Label(window, text="CHATBOT JEFF\n\n", bg="cornflower blue", font=(24))
lblTitle.pack()

#creates intro text
lblDesc = tkinter.Label(window, text="Welcome to Chatbot-Jeff\n\nThis chatbot was created by ALL group A1\n\n\n", bg="cornflower blue")
lblDesc.pack()

#creates the button (currently a non-functional button)
btnBegin = tkinter.Button(window, text="Click To Launch Chatbot")
btnBegin.pack()

window.mainloop()
