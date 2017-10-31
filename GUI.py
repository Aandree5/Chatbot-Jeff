import tkinter
import Get_Functions

window = tkinter.Tk()
window.title("Chatbot Jeff")
window.geometry("600x800")
window.configure(background="cornflower blue")

lblTitle = tkinter.Label(window, text="CHATBOT JEFF\n\n", bg="cornflower blue", font=(24))
lblTitle.pack()

lblDesc = tkinter.Label(window, text="Welcome to Chatbot-Jeff\n\nThis chatbot was created by ALL group A1\n\n\n", bg="cornflower blue")
lblDesc.pack()

btnBegin = tkinter.Button(window, text="Click To Launch Chatbot")
btnBegin.pack()

window.mainloop()
