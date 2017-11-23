import socket
import tkinter as tk
import tkHyperlinkManager as tkHLM
import webbrowser

def chatbotExit(): #Richard
    ''' Sends a message to the server to notify it that the chatbot is
        quitting and then closes the interface and allows other functions
        to end properly'''
    exitMessage = "END"
    thisSocket.send(exitMessage.encode())
    window.quit() #Closes the GUI window which then leads to the rest of the program being able to end as mainloop() terminates
    return None

def receiveMessage(i): #Richard
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage and displays the recieved messages on the user
        interface'''
    
    if i == 0:
        global username
        username = "User"
    
    message = thisSocket.recv(1024).decode()
    while (message != "EndOfMessage"):
        if username == "User" and "YOURNAMEWILLBE" in message: #Checks if username has been changed and for tag identifying new name
            nameholder = message.split()[1:]
            username = ''.join(nameholder)
            username = username.title()  #Assigns username
            thisSocket.send("Received".encode())
            message = thisSocket.recv(1024).decode()
            continue
        
        if "https://" in message or "http://" in message:
            searchLink = message
            hyperlinkObj = tkHLM.HyperlinkManager(chatHistory)

            #This function is now local to remove the need to pass an argument which
            #was breaking the external code used to manage the hyperlinks
            def openLink(): #Richard
                ''' Opens the link sent by the server'''
                webbrowser.open(searchLink, new=2)
            
            chatHistory.configure(state="normal")
            chatHistory.insert(tk.END, "Click here", hyperlinkObj.add(openLink)) #broken line
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

# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect(("127.0.0.1",5001))

i = 0 #Counter used later to prevent the global variable username being reset

#GUI Start
window = tk.Tk() #Creates the main window for the interface
window.title("Chatbot Jeff")
window.geometry("600x550")
window.configure(background="cornflower blue")

lblTitle = tk.Label(window, text="CHATBOT JEFF", bg="cornflower blue", font=("Helvetica", 24)) #Main title for the chatbot GUI
lblTitle.pack()

lbl = tk.Label(window, text="\nChatHistory", bg="cornflower blue", font=("Helvetica", 16)) #Title that sits above the chat history text widget
lbl.pack()

chatHistory = tk.Text(window) #Creates the text window that will be used to show the chat history
chatHistory.pack(padx=30)
chatHistory.configure(state="disabled") #Prevents the user from typing directly into the chat history

userInputFrame = tk.Frame(window) #Creates a frame to hold the widgets related to user input
userInputFrame.configure(background="cornflower blue")

userInput = tk.Entry(userInputFrame, width=75) #Adds a text entry widget to the frame
userInput.grid(row=0, column=0, ipady=3, padx=2)
userInput.bind("<Return>", sendMessage) #Binds the return key to the widget so that it calls the sendMessage function when the key is pressed

sendBtn = tk.Button(userInputFrame, text="Send Message", command=sendMessage) #Adds a button widget that sends the message found in the entry widget to the server
sendBtn.grid(row=0, column=1)
userInputFrame.pack(pady=15) #Adds the frame and its contents to the GUI so it is displayed with the rest of the elements
#GUI End

receiveMessage(i) #Receives the initial message from the chatbot
i = i + 1   #Used to prevent global variable username being reset after initial declaration

tk.mainloop() #Runs the GUI

#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

    


