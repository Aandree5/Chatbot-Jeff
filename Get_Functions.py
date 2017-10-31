import random
from DataAPI import getQuestion, opentDBCats

greetings = ["hi","hello","hey","sup","howdy","henlo","waddup","wassup","heyo","hiya"]

randomStuff = ["Cherophobia is the fear of fun","A flock of crows is called a murder",
               "A single cloud can weight more than 1 million pounds",
               "A crocodile can't stick it's tongue out","A shrimp's heart is in it's head",
               "A pregnant goldfish is called a twit","Rats and horses can't vomit.",
               "If you sneeze too hard, you can fracture a rib.",]

#=========================================================================================================

def getName(sentence):
    """get the name of the user from the inputed sentence"""
    #first - getting rid of unwanted chars
    unwantedChar = [".","'","!","?",","]
    newSentence = ""
    for char in sentence:
        if char not in unwantedChar:
            newSentence = newSentence + char
    newSentence = newSentence.lower() # makes all letters into lowercase - much easier and more efficient
    
    userWords = newSentence.split() #the sentence is split up into words and put into a list

    # ways of introduction:
    # "Hello, my name is ___"
    # "Hi, I'm ____"
    # "Howdy, I'm called ____"
    # Order: Greeting -> pronoun -> Name -> question (optional)
    # eg. "Hello, I'm Jasper. How are you?"
    
    words = ["hi","hello","hey","sup","howdy","henlo","waddup","wassup","heyo","hiya"
             ,"im","i","am","called","my","name","is"] #Single out the name
    
    userName = ""
    for i in range(len(userWords)):     #iterate throught the user's words
        foundWord = False               #sets True when there's a similar word in the other list
        for word in range(len(words)):  #iterates and compares the chosen word from the user's list of words to the words list
            if userWords[i] == words[word] and foundWord == False:
                foundWord = True
        if foundWord == False:
            userName = userName + userWords[i] + " "

    #ask the user if their first word is a greeting
    if userWords[0] not in greetings:
        while True:            
            newGreeting = input('Is your first word a greeting, like "Hello"? \n').lower()
            if newGreeting == "yes":
                greetings.append(userWords[0])
                break
            elif newGreetings == "no":
                break
            else:
                print("Please, type in 'yes' or 'no' \n")
    
    return userName #this is the found name

#=========================================================================================================

def getQuestion():
    """just call this ... I guess, if you want questions ... (need some revision)"""
    cats = opentDBCats(True)
    print("--- Categories ---")
    for i in range(3):
        print(random.choice(cats))
    userInput = input("Please, pick a subject: \n").casefold()


    
    if userInput != "other":
        print("You have chosen: " + userInput.title())
        print("##############################")
        #Input question here XD

    

        question, answer, w, t = getQuestion(userInput, "easy")
    
        userAnswer = input(question)
        if userAnswer.lower() == answer.lower():
            print("Wehey \n")
        elif userAnswer.lower() != answer.lower():
            print("This is not the answer fool!")
            print("The answer is: \n")
            print(answer + "\n")
    elif userInput == "other":
        print("You have chosen: " + userInput.title())
        print("##############################")
        userInput = input("Want to hear a joke, fun fact or something random? \n")
        if userInput == "Yes" or userInput == "yes":
            print(random.choice(randomStuff) + "\n")

#=========================================================================================================

#-----------------
#testing zone
#-----------------
