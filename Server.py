import socket
import time
import random
from DataAPI import getQuestion, getCategories
from determineUserInput import determineUserInput

# Create Socket and bind server to socket
thisSocket = socket.socket()
thisSocket.bind(("127.0.0.1", 5001))
# Listen for clients
thisSocket.listen(1)
# Connect to client
conn, addr = thisSocket.accept()
print ("The Connection ip is : " + str(addr))
print(conn)

def sendMessage(message, EOM = True):
    ''' Given a message input, and a False value, send the message and the
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
        
    answerUserInput = determineUserInput(message)
    
    return(answerUserInput)

def askSomething(answerType, sendMessages, noAnswers, defaultAnswer):
    ''' With input of the type of answer code expected and a string question,
        a list of sentences if not expected answer, and the default fallback
        answer returns the answer to the question '''

    for i, item in enumerate(sendMessages):
        sendMessage(item, (True if i == len(sendMessages) - 1 else False))
        
    answer = receiveMessage()
    print(answer)
    while ((answer[1] != answerType and len(noAnswers) > 0) or
           ((answer[0] == "" or answer[1] in [0, 2, 3, 4]) and len(noAnswers) > 0)):
        
        if(answerType == -1 and answer[1] == 0):
            for cat in sendMessages:
                if (answer[0].casefold() == cat.casefold()):
                    answer = (answer[0], -1)
                    break
            break
        
        if (answer[1] in [2, 4]): # If the user asked a how or are question
            sendMessage(answer[0], False)
            sendMessage(noAnswers[0])
            noAnswers.pop(0)
        elif (answer[1] == 3): # If the user  asked a what question
            sendMessage("The answer to that is {}.".format(answer[0]), False)
            sendMessage(noAnswers[0])
            noAnswers.pop(0)
        elif (answer[1] == 7): # If the user doesn't want to answer
            sendMessage("You should, it would be more fun!")
            noAnswers.pop(len(noAnswers) - 1)
        else:
            sendMessage("Sorry I didn't undertood that.", False)
            sendMessage("Can you repeat please.")

        answer = receiveMessage()
            

    if (answer[1] != answerType):
        answer = (defaultAnswer, 0)

    return (answer[0])

def qChallenge():
    ''' Output a set of questions with a category choosen by the user '''
    cat = getCategories(True, 3)
    if ("Error" in cat):
        sendMessage("{}: {}".format(cat[0], cat[1]), False)
        if (cat[1] == 7):
            sendMessage("Lets try again.")
            return(True)
        else:
            return(False)
    
    receivedMessage = askSomething(-1, ["Pick a subject.", cat[0], cat[1], cat[2]],
                ["You can choose a category from the list above, like 'Music'.",
                 "Hmmm, I see you are afraid of making a mistake."], "Any")
    
    
    # Get a question and answers, from the user choice
    questionSet = getQuestion(receivedMessage, "")
    if ("Error" in questionSet):
        sendMessage(questionSet[1], False)
        sendMessage("Lets try again.", False)
        return (True)

    # If question set of multiple type
    if (questionSet["Type"] == "multiple"):
        receivedMessage = askSomething(5, [questionSet["Question"],
                                           "A: {}".format(questionSet["A"]),
                                           "B: {}".format(questionSet["B"]),
                                           "C: {}".format(questionSet["C"]),
                                           "D: {}".format(questionSet["D"])],
                        ["You can choose one of the options.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
    # If question set of boolean type
    else:
        receivedMessage = askSomething(5, [questionSet["Question"],
                                           "A: {}".format(questionSet["A"]),
                                           "B: {}".format(questionSet["B"])],
                        ["You can choose one of the options.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
        
    if (receivedMessage[0].casefold() == questionSet["corrAnswer"].casefold()):
        sendMessage("Congratulations! That was the right answer!!", False)
        sendMessage("-" * 50, False)
        
        receivedMessage = askSomething(6, ["Would you like to answer another question?"],
                        ["Are you afraid?? :D.",
                        "Hmmm, I see you are afraid of making a mistake."], "No")
        
        if (receivedMessage[0].casefold() == "No".casefold()):
            return (False)
        else:
            sendMessage("Awesome! Lets see if you know the next one.", False)
            return (True)
    else:
        sendMessage("Nice try, but that's not the right answer.", False)
        sendMessage("The right answer was {} ({})."
                    .format(questionSet["corrAnswer"],
                            questionSet[questionSet["corrAnswer"]]), False)
        sendMessage("I know you can get the next one!!", False)
        sendMessage("-" * 50, False)
        
        receivedMessage = askSomething(6, ["Would you like to answer another question?"],
                        ["Are you afraid?? :D.",
                        "Hmmm, I see you are afraid of making a mistake."], "No")
        
        if (receivedMessage[0].casefold() == "No".casefold()):
            return (False)
        else:
            sendMessage("Great! Lets try again.", False)
            return(True)



    
# Say hi to client and get name
clientName = askSomething(1, ["Hi! I am Jeff.", "I can give really nice challanges!", "What's your name?"],
                              ["I would prefer to know your name.",
                              "I see you don't want to tell me."], "Mr. Nobody")

sendMessage("YOURNAMEWILLBE " + clientName, False)

sendMessage("So, {}, I will teach you something today!"
                .format(clientName.title()), False)

cont = True
while cont:
    
        # Get questions for user
    cont = qChallenge()


sendMessage("See you next time! Bye!")
conn.close()
