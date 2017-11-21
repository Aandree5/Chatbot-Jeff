import socket
import tkinter as tk
import tkHyperlinkManager as tkHLM
import webbrowser

# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect(("127.0.0.1",5001))

def chatbotExit(): #Richard
    ''' Sends a message to the server to notify it that the chatbot is
        quitting and then closes the interface and allows other functions
        to end properly'''
    exitMessage = "END"
    thisSocket.send(exitMessage.encode())
    userInput.delete(0, tk.END)
    window.quit()
    return None

def openLink(url): #Richard
    ''' Opens the link sent by the server'''
    webbrowser.open(url, new=2)

def receiveMessage(i): #Richard
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage and displays the recieved messages on the user
        interface'''
    
    if i == 0:
        global username
        username = "User"
    
    message = thisSocket.recv(1024).decode()
    print(message)
    while (message != "EndOfMessage"):
        if username == "User" and "YOURNAMEWILLBE" in message: #Checks if username has been changed and for tag identifying new name
            nameholder = message.split()[1:]
            username = ''.join(nameholder)
            username = username.title()  #Assigns username
            thisSocket.send("Received".encode())
            message = thisSocket.recv(1024).decode()
            continue
        
        if "https://" in message:
            searchLink = message
            hyperlinkObj = tkHLM.HyperlinkManager(chatHistory)
            chatHistory.configure(state="normal")
            chatHistory.insert(tk.END, "Click here", hyperlinkObj.add(openLink(url))) #broken line
            chatHistory.insert(tk.END, "\n")
            chatHistory.configure(state="disabled")
            thisSocket.send("Received".encode())
            message = thisSocket.recv(1024).decode()
            
        chatHistory.configure(state="normal")
        thisSocket.send("Received".encode())
        chatHistory.insert(tk.END, "Jeff: " + message + "\n")
        chatHistory.see(tk.END)
        chatHistory.configure(state="disabled") #prevents user from editing the chat history
        message = thisSocket.recv(1024).decode()

def sendMessage(event=None): #Richard
    '''Waits for the user to enter a messasge in the text entry box in the
       interface and then takes this input from the user and feeds it to the
       chatbot/server, allowing it to respond to the input appropriately.'''

    sMessage = userInput.get()
    if sMessage is None or sMessage == "": #Checks if the user has actually entered anything before sending
        return None #Ends the function before any message is sent to prevent sending of blank message

    if sMessage.lower() == "exit" or sMessage.lower() == "quit" or sMessage.lower() == "goodbye":  #Allows the user to exit the chatbot
        chatbotExit()
        return None

    thisSocket.send(sMessage.encode())
    chatHistory.configure(state="normal")
    chatHistory.insert(tk.END, username + ": " + sMessage + "\n")
    chatHistory.see(tk.END)
    chatHistory.configure(state="disabled")
    userInput.delete(0, tk.END)
    receiveMessage(i)

i = 0 #Counter used later to prevent the global variable username being reset

#GUI Start
window = tk.Tk() #Creates the main window for the interface
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

userInput = tk.Entry(window, width=50)
userInput.pack(pady=15)
userInput.bind("<Return>", sendMessage)

sendBtn = tk.Button(window, text="Send Message", command=sendMessage)
sendBtn.pack(side="right", pady=15)
#GUI End

receiveMessage(i) #Receives the initial message from the chatbot
i = i + 1   #Used to prevent global variable username being reset after initial declaration

tk.mainloop() #Runs the GUI

#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

    


