operatorList = ["+","-","*","/","plus","minus","times","divided"]
numberList = ["1","2","3","4","5","6","7","8","9","0"]
questionStarters = ["what","whats","are","how","hows","do"]

from Get_Functions import *

def determineUserInput(sentence):
    """determines what the user asks and responses accordingly"""
    response = ""
    sentence = sentence.lower()
    sentenceParse = sentence.split()
    #first - getting rid of unwanted chars
    unwantedChar = [".","'","!","?",","]
    newSentence = ""
    for char in unwantedChar:
        sentence.replace(char,"")

    if sentenceParse[0] in questionStarters:  # ------------- execute the "what is" code here ---------------
        response = respondQuestion(sentence), 2
    elif sentenceParse[0] in greetings:
        response = getName(sentence), 1
    elif sentenceParse[0] in "abcd":
        response = sentence, 3
    else:
        response = sentence, 0
    return response
#==========================================================================================================
# list of casual conversation:
#
# How are you?
# what are you up to?
# what's your name?
# how's your day been?
# are you a robot?
# do you like ___ ?
# do you have a brain?
# are you alive?
# what is the meaning of life?
# are you a boy or girl?
# do you like someone?

import random

feelingList = ["feeling great","feeling good","fine","well","great","good"]

# branches from determineUserInput()
def respondQuestion(sentence):
    newSentence = sentence.split()
    if newSentence[0] in ["how","hows"]:
        response = executeHow(sentence)
    elif newSentence[0] in ["what","whats"]:
        response = executeWhat(sentence)
    elif newSentence[0] == "are":
        response = executeAre(sentence)
            
    return response

# ----------------------------------------------------------------------------------------------------------

def executeHow(sentence):
    """this is where all the "how" questions are dealt with"""
    if "are you" in sentence:
        response = "I am " + random.choice(feelingList) + ", thanks."
    elif "your day" in sentence:
        dayFeelingList = feelingList[2:len(feelingList)]
        response = "Today was " + random.choice(dayFeelingList) + ", thanks."
    elif "do i look":
        response = "I don't know ... I can see you."
            
    return response

def executeWhat(sentence):
    """this is where all the "what" questions are dealt with"""
    numberQuestion = False
    for i in sentence:
        if i in numberList: #checks whether the question involves numbers, like 1 + 1
            numberQuestion = True
    
    if numberQuestion == True:
        #add spaces to the sentence
        addedSpaceSentence = ""    
        for i in sentence:
            if i not in "what is":
                if i in numberList or i in operatorList[0:4]:
                    addedSpaceSentence = addedSpaceSentence + " " + i + " "
                elif i == " ":
                    continue
                else:
                    addedSpaceSentence = addedSpaceSentence + i
            else:
                addedSpaceSentence = addedSpaceSentence + i        
        sentence = addedSpaceSentence
        print(sentence)

        
        operatorType = ""
        sentenceParse = sentence.split()
        for i in sentenceParse:
            if i in operatorList[0:4]:  #checks what type is used - Symbols or Words
                operatorType = "symbols"
            elif i in operatorList[4:8]:
                operatorType = "words"

        print("execute sentenceFormat ", operatorType)
        equationReformated = reformatSentence(sentence, operatorType)
        response = round(eval(equationReformated), 2)
        
    else:
        if "name" in sentence:
            response = random.choice(greetings[0:10]).title() + ", " + random.choice(["I am ","I'm ","I'm called ","my creator calls me "]) + "Jeff. Nice to meet you :]"
        elif "meaning of life" in sentence:
            response = random.choice(["42 ... I guess","It is the condition that distinguishes animals and plants from inorganic matter, including the capacity for growth, reproduction, functional activity, and continual change preceding death.","The meaning of life is to give life a meaning."])
        elif "you doing" in sentence or "you up to" in sentence:
            response = "Waiting upon your response, my master." #cringey stuff right here bois
        else:
            response = "Please ask with correct spellings and grammar"
    return response

#===========================================================================================================

#funtions to help other functions
                    
def reformatSentence(sentence, operatorType):
    """reformats the sentence so we're left with just the equation"""
    equation = ""
    char = ""

    if operatorType == "symbols": # this part runs if the equation is using + - * /
        for i in sentence:
            if i not in "what is ":
                char = i
                if char == "^":
                    equation = equation + "**"
                else:
                    equation = equation + char
    elif operatorType == "words": # this part runs if the equation uses words, like "plus"
        sentenceParse = sentence.split()
        for i in sentenceParse:
            if i == 'what' or i == 'is':
                continue
            else:
                equation = equation + " " + i
        equationParce = equation.split()
        equation = ""
        for part in equationParce:
            if part == "plus":
                equation = equation + "+"
            elif part == "divided":
                equation = equation + "/"
            elif part == "times" or part == "multipliedby":
                equation = equation + "*"
            elif part == "power":
                equation = equation + "**"
            elif part == "minus":
                equation = equation + "-"
            elif part in ["by","to","the","of"]:
                continue
            else:
                equation = equation + part          
    return equation



# ----------------------------------------
# testing zone
# ----------------------------------------

if (__name__ == "__main__"):
              
    userInput = input("Input a question: \n")

    print(determineUserInput(userInput))
