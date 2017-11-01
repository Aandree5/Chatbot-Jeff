operatorList = ["+","-","*","/","plus","minus","times","divided"]
numberList = ["1","2","3","4","5","6","7","8","9","0"]

from Get_Functions import *

def determineUserInput(sentence):
    """determines what the user asks and responses accordingly"""
    response = ""
    sentence = sentence.lower()
    sentenceParce = sentence.split()
    if "what" in sentence:  # ------------- execute the "what is" code here ---------------
        response =executeWhatFunction(sentence)
        return response
    elif sentenceParce[0] in greetings:
        return getName(sentence)
           
    else:
        return sentence

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
        sentenceParce = sentence.split()
        for i in sentenceParce:
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

def executeWhatFunction(sentence):
    numberQuestion = False
    for i in sentence:
        if i in numberList: #checks whether the question involves numbers, like 1 + 1
            numberQuestion = True
                
    if numberQuestion == True:
        operatorType = ""
        sentenceParce = sentence.split()
        for i in sentenceParce:
            if i in operatorList[0:4]:  #checks what type is used - Symbols or Words
                operatorType = "symbols"
            elif i in operatorList[4:8]:
                operatorType = "words"
                    
        equationReformated = reformatSentence(sentence, operatorType)
        response = round(eval(equationReformated), 2)
        return response
        
    else:
        response = "Please ask with correct spellings and grammar"
        return response
    
# ----------------------------------------
# testing zone
# ----------------------------------------

if (__name__ == "__main__"):
              
    userInput = input("Input a question: \n")

    print(determineUserInput(userInput))
