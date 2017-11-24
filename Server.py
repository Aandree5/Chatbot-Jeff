import socket
import time
import random
from DataAPI import getQuestion, getCategories, getBirthday, getHistory, getQuote
from determineUserInput import determineUserInput

def sendMessage(message, EOM = True): # Andre
    ''' Given a message input, and a False value, send the message and the
        client keeps wayting for another message '''
    resp = ""
    while (resp != "Received"):             # Check if the client received the message.
        conn.send(str(message).encode())    # Send message to client.
        print("SERVER: {}".format(message)) # Print the message sent.
        resp = conn.recv(1024).decode()     # Waits for client feedback 
    if (EOM):                               # If this is the last message to be sent
        conn.send("EndOfMessage".encode())  # Send a key word to the client to stop listening

def receiveMessage(): # Andre
    ''' Receive a message from the client and check if received correctly,
        returns the message '''
    message = conn.recv(1024).decode()
    if not message: # If message is empty, try to receive again
        sendMessage("Sorry, I couldn't get that, can you repeat?")
        message = conn.recv(1024).decode()
        if not message: # If message is empty again, send message and exit
            sendMessage("Sorry, I not able to receive that, plese try again another day.")
            exit()
            
    if (message != "END"): # Check if the user want to end the conversation
        print ("CLIENT: {}".format(message))
            
        answerUserInput = determineUserInput(message)
    else:
        answerUserInput = message
    
    return(answerUserInput)

def askSomething(answerType, sendMessages, noAnswers, defaultAnswer): # Andre
    ''' With input of the type of answer code expected and a list of messages to send,
        another of sentences if not expected answer, and the default fallback
        answer returns the answer to the question '''

    for i, item in enumerate(sendMessages): # Send all the messages to client
        sendMessage(item, (True if i == len(sendMessages) - 1 else False))
        
    answer = receiveMessage()
    if (type(answer) != tuple): # If the answer if for exemple "END" just return it
        return(answer)
    
    while ((answer[1] != answerType or answer[0] == "")  and len(noAnswers) > 0):
        
        if(answerType == -1):
            for cat in sendMessages:
                if (cat.casefold() in answer[0].casefold()):
                    answer = (cat, -1)
                    break
            break

        if (answer[1] == 2): # If the user asked a question
            if (type(answer[0]) == tuple): # Send two messages, i.e. the text and the link of the google search 
                sendMessage(answer[0][0], False)
                sendMessage(answer[0][1], False)
            else:
                sendMessage(answer[0], False)
                
            sendMessage(noAnswers[0])
            noAnswers.pop(0)
        elif (answer[1] == 5): # If the user doesn't want to answer
            sendMessage("You should, it would be more fun!")
            noAnswers.pop(len(noAnswers) - 1)
        elif (answer[1] != answerType):
            sendMessage("Sorry I didn't undertood that.", False)
            sendMessage("Can you repeat please.")
            noAnswers.pop(len(noAnswers) - 1)

        answer = receiveMessage()
            

    if (answer[1] != answerType):
        if (answer[1] == 2):
            sendMessage(answer[0], False)            
        answer = (defaultAnswer, 0)

    return (answer[0])

def oneQuestion(qType): # Andre
    ''' Input of type of question as string Output a set of
        a question of that type '''
    if (qType == "OpentDB"):
        cat = getCategories(True, 3)
        if ("Error" in cat):
            sendMessage("{}: {}".format(cat[0], cat[1]), False)
            return(cat)
            
        receivedMessage = askSomething(-1, ["Pick a subject.", cat[0], cat[1], cat[2]],
                    ["You can choose a category from the list above, like 'Music'.",
                     "Hmmm, I see you are afraid of making a mistake."], "Any")
    else:
       receivedMessage = "" # Create the variable anyway, because it can be another type of question
    
    # Get a question and answers, from the user choice
    questionSet = getQuestion(receivedMessage, "", 1, qType)[0]
    if ("Error" in questionSet):
        sendMessage("{}: {}".format(questionSet[0], questionSet[1]), False)
        return(questionSet)
    
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
        
    # If question set of Birthday or History or Quote type
    elif (questionSet["Type"] in ["Birthday"], "History", "Quote"):
        receivedMessage = askSomething(0, [questionSet["Question"]],
                        ["You can try a random answer if felling lucky.",
                        "Hmmm, I see you are afraid of making a mistake."], "X")
        questionSet[receivedMessage.upper()] = receivedMessage


    if (questionSet[receivedMessage.upper()] == questionSet["corrAnswer"]):
        sendMessage("Congratulations! That was the right answer!!", False)
        sendMessage("-" * 50, False)
    else:
        sendMessage("Nice try, but that's not the right answer.", False)
        sendMessage("The right answer was {}.".format(questionSet["corrAnswer"]), False)
        sendMessage("I know you can get the next one!!", False)
        sendMessage("-" * 50, False)


def quizChallange(nrQuestions): # Andre
    ''' With input of a number of questions, output a list of question sets
        with the lenght of the choosen input '''
    if (nrQuestions < 1 or nrQuestions > 50):
        sendMessage("For a Quiz challenge ou have to choose between 2 and 50 quesitons.")
        return(nrQuestions)

    cat = getCategories(True, 3)
    if ("Error" in cat):
        sendMessage("{}: {}".format(cat[0], cat[1]), False)
        return(cat)
    
    receivedMessage = askSomething(-1, ["Pick a subject.", cat[0], cat[1], cat[2]],
                ["You can choose a category from the list above, like 'Music'.",
                 "Hmmm, I see you are afraid of making a mistake."], "Any")

    
    # Get a question and answers, from the user choice
    qChaSet = getQuestion(receivedMessage, "", nrQuestions)
    if ("Error" in qChaSet):
        sendMessage("{}: {}".format(qChaSet[0], qChaSet[1]), False)
        return(qChaSet)

    Score = 0 # Initialize the variable to keep track of the right answers

    for questionSet in qChaSet:
        # If question set of multiple type
        if (questionSet["Type"] == "Multiple"):
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
        
        if (questionSet[receivedMessage.upper()] == questionSet["corrAnswer"]):
            sendMessage("Congratulations! That was the right answer!!", False)
            sendMessage("-" * 50, False)
            Score += 1
        else:
            sendMessage("Nice try, but that's not the right answer.", False)
            sendMessage("The right answer was {}.".format(questionSet["corrAnswer"]), False)
            sendMessage("I know you can get the next one!!", False)
            sendMessage("-" * 50, False)

    return(Score)

def funFacts(): # Andre
    ''' With no input, output one fun fact '''

    fType = random.choice(["Birthday", "History", "Quote"])
    
    if (fType == "Birthday"):
        fact = getBirthday()[0]
        sendMessage("I know that {} was born in {}.".format(fact["Name"], fact["Date"]), False)
        
    elif (fType == "History"):
        fact = getHistory()[0]
        sendMessage("I found that '{}' in {}.".format(fact["Event"], fact["Date"]), False)
        
    elif (fType == "Quote"):
        fact = getQuote()[0]
        sendMessage("I know that {} said '{}'.".format(fact["Name"], fact["Quote"]), False)



#   Start server   #     
####################
#                  #
#    CONNECTION    #
#                  #
####################       
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
if (clientName == "END"):
    sendMessage("See you next time! Bye!")
    conn.close()
    thisSocket.close
    exit()

sendMessage("YOURNAMEWILLBE " + clientName, False)

message = askSomething(0, ["So, {}, I will teach you something today!".format(clientName.title()),
                           "Would you like a 'challenge' or maybe just a 'fun fact'?"],
                       ["You can ask for a 'Question challenge' or even a 'fun fact'.",
                        "If you want you could go for a 'Quiz Challenge'!"], None)
    
while True:
    if (type(message) == str and "question challange".casefold() in message.casefold()):
        oneQuestion("OpentDB")
    elif (type(message) == str and "quiz challange".casefold() in message.casefold()):
        nr = askSomething(0, ["How many questions would you like to answer?"],
                              ["Pick a number between 2 and 50."], "5")
        
        score = quizChallange(int(nr))
        
        sendMessage("You got {} out of {} quesions right!".format(score, nr), False)

    elif (type(message) == str and "birthday challange".casefold() in message.casefold()):
        oneQuestion("Birthday")
        
    elif (type(message) == str and "history challange".casefold() in message.casefold()):
        oneQuestion("History")
        
    elif (type(message) == str and "quote challange".casefold() in message.casefold()):
        oneQuestion("Quote")

    elif (type(message) == str and "fun fact".casefold() in message.casefold()):
        funFacts()
        
    elif (type(message) == str and "challange".casefold() in message.casefold()):
        message = askSomething(0, ["You can ask for a question, quiz, history, birthday or quote challange."],
                               ["You can ask me anything else, I will try to help you."], None)
        continue
    
    elif (message == "END"):
        break

    
    message = askSomething(0, ["If you want you can ask anything!"],
                       ["You can ask me anything, I will try to help you."], None)



sendMessage("See you next time! Bye!")
conn.close()
thisSocket.close
exit()
