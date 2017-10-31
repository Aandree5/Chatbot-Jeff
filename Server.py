import socket
import time
import random
from DataAPI import getQuestion, getCategories
from Get_Functions import getName

# Create Socket and bind server to socket
thisSocket = socket.socket()
thisSocket.bind(("127.0.0.1", 5001))
# Listen for clients
thisSocket.listen(1)
# Connect to client
conn, addr = thisSocket.accept()
print ("The Connection ip is : " + str(addr))

def sendMessage(message, EOM = True):
    ''' Given a message input, and a Flase value, send the message and the
        client keeps wayting for another message '''
    resp = ""
    if (EOM):
        while (resp != "Received"): # If client doesn't receive message, send again
            conn.send(message.encode())
            print("SERVER: {}".format(message))
            resp = conn.recv(1024).decode() # Waits for client feedback 
        conn.send("EndOfMessage".encode())
    else:
        while (resp != "Received"): # If client doesn't receive message, send again
            conn.send(message.encode())
            print("SERVER: {}".format(message))
            resp = conn.recv(1024).decode() # Waits for client feedback 

def receiveMessage():
    ''' Receive a message from the client and check if received correctly,
        returns the message '''
    message = conn.recv(1024).decode()
    if not message: # If message is None, try to receive again
        sendMessage("Sorry, I couldn't get that, can you repeat?")
        message = conn.recv(1024).decode()
        if not message: # Couldn't receive message, exit
            sendMessage("Sorry, I not able to receive that, plese try again another day.")
            exit()
    print ("CLIENT: {}".format(message))
    return(message)
    

receiveMessage()

# Say hi to client and get name
sendMessage("Hi! What's your name?")
clientName = getName(receiveMessage())

sendMessage("So, {}, I will teach you something today!"
            .format(clientName.title()), False)
sendMessage("Pick a subject.", False)
cat = getCategories(True, 3)
sendMessage(cat[0], False)
sendMessage(cat[1], False)
sendMessage(cat[2])

while True:
    receivedMessage = receiveMessage()

    # Get a question and answers, from the user choice
    questionSet = getQuestion(receivedMessage, "")
    if ("Error" in questionSet):
        sendMessage(questionSet[1], False)
        sendMessage("Try again.")
        continue

    print(questionSet)
    
    if (questionSet["Type"] == "multiple"):
        sendMessage(questionSet["Question"], False)
        sendMessage("A: {}".format(questionSet["A"]), False)
        sendMessage("B: {}".format(questionSet["B"]), False)
        sendMessage("C: {}".format(questionSet["C"]), False)
        sendMessage("D: {}".format(questionSet["D"]))
    else:
        sendMessage(questionSet["Question"], False)
        sendMessage("A: {}".format(questionSet["A"]), False)
        sendMessage("B: {}".format(questionSet["B"]))
        
    receivedMessage = receiveMessage()
    if (receivedMessage.casefold() == questionSet["corrAnswer"].casefold()):
        sendMessage("Congratulations! That was the right answer!!", False)
        sendMessage("-" * 50, False)
        sendMessage("Would you like to answer another question?")
        
        receivedMessage = receiveMessage()
        if (receivedMessage.casefold() == "No".casefold()):
            break
        else:
            sendMessage("Pick a new subject.", False)
            cat = getCategories(True, 3)
            sendMessage(cat[0], False)
            sendMessage(cat[1], False)
            sendMessage(cat[2])
    else:
        sendMessage("Nice try, but that's not the right answer.", False)
        sendMessage("The right answer was {} ({})."
                    .format(questionSet["corrAnswer"],
                            questionSet[questionSet["corrAnswer"]]), False)
        sendMessage("I know you can get the next one!!", False)
        sendMessage("-" * 50, False)
        sendMessage("Would you like to answer another question?")
        
        receivedMessage = receiveMessage()
        if (receivedMessage.casefold() == "No".casefold()):
            break
        else:
            sendMessage("Pick a new subject.", False)
            cat = getCategories(True, 3)
            sendMessage(cat[0], False)
            sendMessage(cat[1], False)
            sendMessage(cat[2])



sendMessage("See you next time! Bye!")
conn.close()
