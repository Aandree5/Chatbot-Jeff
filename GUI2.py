import tkinter as tk
import determineUserInput as detUsrIn

window = tk.Tk()
window.title("Chatbot Jeff")
window.geometry("600x600")
window.configure(background="cornflower blue")

lblTitle = tk.Label(window, text="CHATBOT JEFF\n\n", bg="cornflower blue", font=(24))
lblTitle.pack()

userInput = tk.Entry(window)
userInput.pack()

lbl = tk.Label(window, text="\nChatHistory", bg="cornflower blue")
lbl.pack()

def cb(event):
    userText = userInput.get()
    botText = str(detUsrIn.determineUserInput(userText)[0])
    userInput.delete(0, tk.END)
    msgBox.configure(state="normal")
    msgBox.insert(tk.END, "User: " + userText + "\n")
    msgBox.insert(tk.END, "Jeff: " + botText + "\n")
    msgBox.configure(state="disabled")
    return 0

userInput.bind("<Return>", cb)
msgBox = tk.Text(window)
msgBox.pack()
msgBox.configure(state="disabled")

tk.mainloop()
