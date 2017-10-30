import socket
import time
import random
from DataAPI import getQuestion, opentDBCat

#### Start the server
host = "127.0.0.1"
port = 5001
# Create Socket and bind server to socket
thisSocket = socket.socket()
thisSocket.bind((host, port))
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
    

# Say hi to client amd get his name
sendMessage("Hi! What's your name?")
clientName = receiveMessage()

sendMessage("So, {} choose a category for today?".format(clientName.title()))

while True:
    receivedMessage = receiveMessage()

    # Get a question and answers, from the user choice
    data = getQuestion(receivedMessage, "")
    if ("Error" in data):
        sendMessage(data[1], False)
        sendMessage("Try again.")
        continue

    question, answer, wrong, qType = data

    if (qType == "bollean"):
        # Mix right answer and the worng one
        ansList = [answer, wrong]
        random.shuffle(ansList)
        sendMessage("{}".format(question), False)
        sendMessage("{}".format(ansList[0]), False)
        sendMessage("{}".format(ansList[1]), False)
    else:
        # Mix right answer in the worng ones
        wrong.append(answer)
        random.shuffle(wrong)
        sendMessage("{}".format(question), False)
        sendMessage("{}".format(wrong[0]), False)
        sendMessage("{}".format(wrong[1]), False)
        sendMessage("{}".format(wrong[2]), False)
        sendMessage("{}".format(wrong[3]))

    receivedMessage = receiveMessage()
    if (answer.casefold() == receivedMessage.casefold()):
        sendMessage("Congratulations! That was the right answer!!", False)
        sendMessage("-" * 50, False)
        sendMessage("Would you like to answer another question?")
        
        receivedMessage = receiveMessage()
        if (receivedMessage.casefold() == "No".casefold()):
            break
        else:
            sendMessage("Choose a category.")
    else:
        sendMessage("Nice try, but that's not the right answer.", False)
        sendMessage("The right answer is {}.".format(answer), False)
        sendMessage("-" * 50, False)
        sendMessage("Would you like to answer another question?")
        
        receivedMessage = receiveMessage()
        if (receivedMessage.casefold() == "No".casefold()):
            break
        else:
            sendMessage("Choose a category.")



sendMessage("See you next time! Bye!")
conn.close()
