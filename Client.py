import socket

#### Connection to Server 
host = '127.0.0.1'
port = 5001
# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect((host,port))

def receiveMessage():
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage '''
    message = thisSocket.recv(1024).decode()
    while (message != "EndOfMessage"):
        print("Server: {}".format(message))
        thisSocket.send("Received".encode())
        message = thisSocket.recv(1024).decode()
    
receiveMessage()
while True:
    sendMessage = input("Send: ")
    if (sendMessage is None or sendMessage == ""):
        continue
    if (sendMessage == "end"):
        break
    thisSocket.send(sendMessage.encode())
    receiveMessage()
    
#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

