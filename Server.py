import socket
import time
import random
from DataAPI import getQuestion, getCategories
from determineUserInput import determineUserInput

def sendMessage(message, EOM = True):
    ''' Given a message input, and a False value, send the message and the
        client keeps wayting for another message '''
    resp = ""
    if (EOM):
        while (resp != "Received"): # If client doesn't receive message, send again
            conn.send(str(message).encode())
            print("SERVER: {}".format(message))
            resp = conn.recv(1024).decode() # Waits for client feedback 
        conn.send("EndOfMessage".encode())
    else:
        while (resp != "Received"): # If client doesn't receive message, send again
            conn.send(str(message).encode())
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
    while (answer[1] != answerType or answer[0] == ""  and len(noAnswers) > 0):
        
        if(answer[1] == 0 and answerType == -1):
            for cat in sendMessages:
                if (answer[0].casefold() == cat.casefold()):
                    answer = (answer[0], -1)
                    break
        elif (answer[1] == 2): # If the user asked a how or are question
            if (type(answer[0]) == str):
                sendMessage(answer[0], False)
            else:
                sendMessage(answer[0][0], False)
                sendMessage(answer[0][1], False)
                
            sendMessage(noAnswers[0])
            noAnswers.pop(0)
        elif (answer[1] == 5): # If the user doesn't want to answer
            sendMessage("You should, it would be more fun!")
            noAnswers.pop(len(noAnswers) - 1)
        else:
            sendMessage("Sorry I didn't undertood that.", False)
            sendMessage("Can you repeat please.")

        answer = receiveMessage()
            

    if (answer[1] != answerType):
        answer = (defaultAnswer, 0)

    return (answer[0])

def oneQuestion(qType):
    ''' Output a set of questions with a category choosen by the user '''
    if (qType == "opentDB"):
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
    else:
       receivedMessage = "" 
    
    # Get a question and answers, from the user choice
    questionSet = getQuestion(receivedMessage, "", 1, qType)
    if ("Error" in questionSet):
        sendMessage(questionSet[1], False)
        sendMessage("Lets try again.", False)
        return (True)

    # If question set of Multiple type
    if (questionSet["Type"] == "Multiple"):
        receivedMessage = askSomething(3, [questionSet["Question"],
                                           "A: {}".format(questionSet["A"]),
                                           "B: {}".format(questionSet["B"]),
                                           "C: {}".format(questionSet["C"]),
                                           "D: {}".format(questionSet["D"])],
                        ["You can choose one of the options.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
    # If question set of Boolean type
    elif (questionSet["Type"] == "Bollean"):
        receivedMessage = askSomething(3, [questionSet["Question"],
                                           "A: {}".format(questionSet["A"]),
                                           "B: {}".format(questionSet["B"])],
                        ["You can choose one of the options.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
    # If question set of Birthday type
    elif (questionSet["Type"] == "Birthday"):
        receivedMessage = askSomething(0, [questionSet["Question"]],
                        ["You can try a random one if felling lucky.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
    # If question set of History type
    elif (questionSet["Type"] == "History"):
        receivedMessage = askSomething(0, [questionSet["Question"]],
                        ["You can try a random one if felling lucky.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
    # If question set of Quote type
    elif (questionSet["Type"] == "Quote"):
        receivedMessage = askSomething(0, [questionSet["Question"]],
                        ["You can try a random one if felling lucky.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")

    print(receivedMessage.casefold())
    print(questionSet["corrAnswer"].casefold())
    if (receivedMessage.casefold() == questionSet["corrAnswer"].casefold()):
        sendMessage("Congratulations! That was the right answer!!", False)
        sendMessage("-" * 50, False)
    else:
        sendMessage("Nice try, but that's not the right answer.", False)
        sendMessage("The right answer was {}."
                    .format(questionSet["corrAnswer"]), False)
        sendMessage("I know you can get the next one!!", False)
        sendMessage("-" * 50, False)


def quizChallange(nrQuestions):
    if (nrQuestions < 1 or nrQuestions > 50):
        sendMessage("For a Quiz challenge ou have to choose between 2 and 50 quesitons.")
        return(True)

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
    qChaSet = getQuestion(receivedMessage, "", nrQuestions)
    if ("Error" in qChaSet):
        sendMessage(qChaSet[1], False)
        sendMessage("Lets try again.", False)
        return (True)

    Score = 0

    for questionSet in qChaSet:
        # If question set of multiple type
        if (questionSet["Type"] == "multiple"):
            receivedMessage = askSomething(3, [questionSet["Question"],
                                               "A: {}".format(questionSet["A"]),
                                               "B: {}".format(questionSet["B"]),
                                               "C: {}".format(questionSet["C"]),
                                               "D: {}".format(questionSet["D"])],
                            ["You can choose one of the options.",
                            "Hmmm, I see you are afraid of making a mistake."], "X")
        # If question set of boolean type
        else:
            receivedMessage = askSomething(3, [questionSet["Question"],
                                               "A: {}".format(questionSet["A"]),
                                               "B: {}".format(questionSet["B"])],
                            ["You can choose one of the options.",
                            "Hmmm, I see you are afraid of making a mistake."], "X")
            
        if (receivedMessage[0].casefold() == questionSet["corrAnswer"].casefold()):
            sendMessage("Congratulations! That was the right answer!!", False)
            sendMessage("-" * 50, False)
            Score += 1
        else:
            sendMessage("Nice try, but that's not the right answer.", False)
            sendMessage("The right answer was {} ({})."
                        .format(questionSet["corrAnswer"],
                                questionSet[questionSet["corrAnswer"]]), False)
            sendMessage("I know you can get the next one!!", False)
            sendMessage("-" * 50, False)

    return(Score)


#### CONNECTION ####
       
# Create Socket and bind server to socket
thisSocket = socket.socket()
thisSocket.bind(("127.0.0.1", 5001))
# Listen for clients
thisSocket.listen(1)
# Connect to client
conn, addr = thisSocket.accept()
print ("The Connection ip is : " + str(addr))
print(conn)

####################
    
# Say hi to client and get name
clientName = askSomething(1, ["Hi! I am Jeff.", "I can give really nice challanges!", "What's your name?"],
                              ["I would prefer to know your name.",
                              "I see you don't want to tell me."], "Mr. Nobody")

sendMessage("YOURNAMEWILLBE " + clientName, False)

message = askSomething(0, ["So, {}, I will teach you something today!"
                .format(clientName.title()), "Would you like a challenge or have any questions?"],
                       ["You can ask for a Question challenge",
                        "If you want you could go for a Quiz Challenge!"], None)
    
while True:
    if (type(message) == str and "question challange".casefold() in message.casefold()):
        oneQuestion("opentDB")
    elif (type(message) == str and "quiz challange".casefold() in message.casefold()):
        nr = askSomething(0, ["How many questions would you like to answer?"],
                              ["Pick a number between 2 and 50."], "5")
        
        score = quizChallange(int(nr))
        
        sendMessage("You got {} out of {} quesions right!".format(score, nr), False)

    if (type(message) == str and "birthday challange".casefold() in message.casefold()):
        oneQuestion("Birthday")
    if (type(message) == str and "history challange".casefold() in message.casefold()):
        oneQuestion("History")
    if (type(message) == str and "quote challange".casefold() in message.casefold()):
        oneQuestion("Quote")
    elif (message == "END"):
        break

    
    message = askSomething(0, ["If you want you can ask anything else!"],
                       ["You can choose more Questions to challenge your self."], None)


sendMessage("See you next time! Bye!")
conn.close()
