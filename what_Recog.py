operatorList = ["+","-","*","/","plus","minus","times","divided"]
numberList = ["1","2","3","4","5","6","7","8","9","0"]

def determineUserInput(sentence):
    """determines what the user asks and responses accordingly"""
    sentence = sentence.lower()
    if "what" in sentence:  # ------------- execute the "what is" code here ---------------
        numberQuestion = False
        for i in sentence:
            if i in numberList: #checks whether the question involves numbers, like 1 + 1
                numberQuestion = True
                
        if numberQuestion == True:
            operatorType = ""
            for i in sentence:
                if i in operatorList[0:4]:  #checks what type is used - Symbols or Words
                    operatorType = "symbols"
                elif i in operatorList[4:len(operatorList)]:
                    operatorType = "words"
                    
            equationReformated = reformatSentence(sentence, operatorType)
            answer = eval(equationReformated)
            return answer
        
        else:
            return "null"


def reformatSentence(sentence,operatorType):
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
        for u in sentence:
            if u not in "what is ":
                char = u
                if char != " ":
                    equation = equation + char
        for part in equation:
            if part == "plus":
                equation = equation + "+"
            elif part == "dividedby":
                equation = equation + "/"
            elif part == "times" or part == "multipliedby":
                equation = equation + "*"
            elif part == "tothepowerof":
                equation = equation + "**"
            elif part == "minus":
                equation = equation + "-"
            else:
                equation = equation + part
    return equation


# ----------------------------------------
# testing zone
# ----------------------------------------
              
userInput = input("Input a question: \n")

print(determineUserInput(userInput))
