import tkinter as tk
import determineUserInput as detUsrIn

def chat(event): #Richard
    '''This function takes the input from the user and feeds it to the chatbot, allowing
       the chatbot to respond to the input appropriately. Essentially this function
       bridges the GUI and chatbot'''
    
    userText = userInput.get()
    if userText == "":
        return 1 #returns 1 to signify empty input
    botText = str(detUsrIn.determineUserInput(userText)[0])
    userInput.delete(0, tk.END)
    chatHistory.configure(state="normal")
    chatHistory.insert(tk.END, "User: " + userText + "\n")
    chatHistory.insert(tk.END, "Jeff: " + botText + "\n")
    chatHistory.see(tk.END)
    chatHistory.configure(state="disabled") #prevents user from editing the chat history
    return 0

window = tk.Tk()
window.title("Chatbot Jeff")
window.geometry("600x600")
window.configure(background="cornflower blue")

lblTitle = tk.Label(window, text="CHATBOT JEFF", bg="cornflower blue", font=("Helvetica", 24))
lblTitle.pack()

lbl = tk.Label(window, text="\nChatHistory", bg="cornflower blue", font=("Helvetica", 16))
lbl.pack()

chatHistory = tk.Text(window)
chatHistory.pack(padx=30)
chatHistory.configure(state="disabled")

userInput = tk.Entry(window)
userInput.pack(pady=15)
userInput.bind("<Return>", chat)

tk.mainloop()
