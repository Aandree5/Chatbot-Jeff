import socket

# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect(("127.0.0.1",5001))

def receiveMessage():
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage '''
    message = thisSocket.recv(1024).decode()
    while (message != "EndOfMessage"):
        print("Jeff: {}".format(message)) #response from server, needs to show on interface
        thisSocket.send("Received".encode())
        message = thisSocket.recv(1024).decode()

    
print ("Connected to Jeff")
receiveMessage()
while True:
    sendMessage = input("Send: ") #input from user, needs to come from interface
    if (sendMessage is None or sendMessage == ""):
        continue
    if (sendMessage == "end"):
        break
    thisSocket.send(sendMessage.encode())
    receiveMessage()
    
#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

