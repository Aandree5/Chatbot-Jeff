import socket
import tkinter as tk

# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect(("127.0.0.1",5001))

finalMessage = []

def receiveMessage():
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage '''
    message = thisSocket.recv(1024).decode()
    
    while (message != "EndOfMessage"):
        print("Jeff: {}".format(message)) #response from server, needs to show on interface
        finalMessage.append(message)
        thisSocket.send("Received".encode())
        message = thisSocket.recv(1024).decode()
    return finalMessage

##
def showChat(event):
    '''This function takes the input from the user and feeds it to the chatbot, allowing
       the chatbot to respond to the input appropriately. Essentially this function
       bridges the GUI and chatbot'''
    
    userText = str(userInput.get())
    if userText == "":
        return 1 #returns 1 to signify empty input
    sendInput(userText)
    botText = str(receiveMessage())
    userInput.delete(0, tk.END)
    chatHistory.configure(state="normal")
    chatHistory.insert(tk.END, "User: " + userText + "\n")

    for message in botText:
        chatHistory.insert(tk.END, "Jeff: " + str(message) + "\n")

    finalMessage = []
    chatHistory.see(tk.END)
    chatHistory.configure(state="disabled") #prevents user from editing the chat history
    return 0

def sendInput(userInput):
    userText = userInput
    return userText

def start():
    botText = str(receiveMessage())
    chatHistory.configure(state="normal")
    chatHistory.insert(tk.END, "Jeff: " + botText + "\n")
    chatHistory.see(tk.END)
    chatHistory.configure(state="disabled")
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
userInput.bind("<Return>", showChat)

start()

tk.mainloop()
##
    
print ("Connected to Jeff")
#receiveMessage()
while True:
    sendMessage = sendInput() #input from user, needs to come from interface
    if (sendMessage is None or sendMessage == ""):
        continue
    if (sendMessage == "end"):
        break
    thisSocket.send(sendMessage.encode())
    receiveMessage()
    
#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

