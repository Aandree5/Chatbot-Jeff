operatorList = ["+","-","*","/","plus","minus","times","divided"]
numberList = ["1","2","3","4","5","6","7","8","9","0"]
questionStarters = ["what","whats","are","how","hows","do","tell", "who", "which"]
notAnswer = ["dont want to", "i dont want to", "its enough", "dont want more"]

from Get_Functions import *

def determineUserInput(sentence):
    """determines what the user asks and responses accordingly"""
    response = ""
    sentence = sentence.lower()
    #first - getting rid of unwanted chars
    unwantedChar = [".","'","!","?",","]
    
    for char in unwantedChar:
        sentence = sentence.replace(char," ")

    sentenceParse = sentence.split()
    if (sentenceParse[0] == "i" and len(sentenceParse) > 1):
        if (sentenceParse[1] == "am"):
            sentenceParse.insert(0, " ".join(sentenceParse[0:2]))

    if sentenceParse[0] in questionStarters:  # ------------- execute the "what is" code here ---------------
        response = respondQuestion(sentence), 2
    elif sentenceParse[0] in greetings:
        response = getName(sentence), 1
    elif sentence in "abcd":
        response = sentence, 3
    elif (sentence.casefold() == "Yes".casefold()) or (sentence.casefold() == "No".casefold()):
        response = sentence, 4  
    elif sentence in notAnswer:
        response = sentence, 5      
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
# Are you real?
# do you like ___ ?
# do you have a brain?
# are you alive?
# what is the meaning of life?
# are you a boy or girl?
# do you like someone?
# do you love someone?
# What time is it?
# What date is it?
# Tell me..
# How old are you?
# How do you work?/How do chatbots work?
# what would you like to be when you grow up?
# Who are you?
# Who is the best person in the world?
# Who founded facebook?
# who is the Queen of England?
# Who is the president of USA?
# Who is God?
# What are you?/ What is a chatbot?
# Who am I?
# Who made you?
# Which is the most popular programming language?
# What is UK capital?
# which is the biggest country in the world?
# which is the smallest country in the world?


import random
from datetime import datetime
now = datetime.now ()
import webbrowser

feelingList = ["feeling great","feeling good","fine","well","great","good"]

randomThings = ["Banging your head against a wall burns 150 calories an hour.",
              "More than 50% of the people in the world have never made or received a telephone call.",
              "Every human spent about half an hour as a single cell.",
              "Guinea pigs and rabbits can't sweat.",
              "You can’t kill yourself by holding your breath"
                ]
randomJokes = ["Knock, knock!/ Who’s there?/ Opportunity!/ That is impossible. Opportunity doesn’t come knocking twice!",
                "Knock knock. / Who’s there? / FBI. / FB…/ We are asking the questions here!",
                "Knock knock. /Who’s there? /The interrupting doctor. / The interr…/ You've got cancer."]



# branches from determineUserInput()
def respondQuestion(sentence):
    newSentence = sentence.split()
    if newSentence[0] in ["how","hows"]:
        response = executeHow(sentence)
    elif newSentence[0] in ["what","whats"]:
        response = executeWhat(sentence)
    elif newSentence[0] == "are":
        response = executeAre(sentence)
    elif newSentence[0] == "tell":
        response = executeTell(sentence) 
    elif newSentence[0]== "do":
        response = executeDo(sentence)
    elif newSentence[0]== "who":
        response = executeWho(sentence)
    elif newSentence[0]=="which":
        response = executeWhich(sentence)
        
    return response

# ----------------------------------------------------------------------------------------------------------
def executeAre(sentence):
    """this is where all the "are" questions are dealt with"""
    if "you alive" in sentence:
        response = "Yes, I'm alive. I'm talking to you right now. What something else would you like to know?"
    elif "a boy or a girl" in sentence:
        response = "My name is Jeff so I'm a boy I guess. Please, ask me more question."
    elif "you real" in sentence:
        response = "I'm talking to you so I exist so yes, I'm real. I'm waiting for your next question"
    elif "a robot" in sentence or "a human" in sentence or "a alien" in sentence:
        response = "Actually I'm a chatbot. If you have more questions, please ask me."
    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None 

    return response


def executeWhich(sentence):
    """this is where all the "which" questions are dealt with"""
    if "popular programming language" in sentence or "best known programming language" in sentence:
        response = "Java is top pick as one of the most popular programming languages, used for building server-side applications to video games and mobile apps. What other things do you want to know?"
    elif "biggest country" in sentence or "largest country" in sentence:
        response = "Russia is the world's largest country. If you have more questions, please ask me."
    elif "smallest country" in sentence:
        response = "Based on landmass, Vatican City is the smallest country in the world, measuring just 0.2 square miles, almost 120 times smaller than the island of Manhattan. Ask me everything you want to know."
    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None
        
    return response


def executeWho(sentence):
    """this is where all the "who" questions are dealt with"""
    if "are you" in sentence:
        response = "I'm Jeff, an awesome chatbot. If you have more questions, please ask me."
    elif "best person" in sentence or "best guy" in sentence or "best human" in sentence:
        response = "Henry Dunant, the founder of the Red Cross. What something else would you like to know?"
    elif "founded facebook" in sentence:
        response = "Facebook was founded by Mark Zuckerberg with his college roommate and fellow Harvard University student Eduardo Saverin. I'm waiting for your next question"
    elif "queen of england" in sentence or "uk queen" in sentence:
        response = "Elizabeth II (born Elizabeth Alexandra Mary; 21 April 1926) has been Queen of the United Kingdom, Canada, Australia, and New Zealand since 6 February 1952. Please, ask me more questions."
    elif "president of usa" in sentence:
        response = "Donald Trump has become the 45th President of the USA since 2016. What something else would you like to know?"
    elif "god" in sentence:
        response = "Einstein believed in a God represented by order, harmony, beauty, simplicity and elegance. Ask me everything you want to know"
    elif "am I" in sentence:
        response = "You're a human, silly guy."
    elif "made you" in sentence or "created you" in sentence or "founded you" in sentence:
        response = "My founders are Jasper, Andres, Suraj and Delia. Please, ask me more questions."
    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None
         
    return response

def executeDo(sentence):
    """this is where all the "do" questions are dealt with"""
    if "like me" in sentence or "love me" in sentence:
        response = "Not really. You are just a human. If you have more questions, please ask me."
    elif "programming" in sentence:
        response = "Of course! Due of it I'm alive. What something else would you like to know?"
    elif "have brain" in sentence:
       response = "No, I'm a robot. Ask me everything you want to know."
    elif "like someone" in sentence:
        response = "I like Rihanna, she is a really good singer. I'm waiting for your next question."
    elif "love someone" in sentence:
        response = "I'm a narcissist so I love myself. What other information would you like to find out?"
    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None        

    return response


def executeHow(sentence):
    """this is where all the "how" questions are dealt with"""
    if "are you" in sentence:
        response = "I am " + random.choice(feelingList) + ", thanks."
    elif "your day" in sentence:
        dayFeelingList = feelingList[2:len(feelingList)]
        response = "Today was " + random.choice(dayFeelingList) + ", thanks."
    elif "do i look" in sentence:
        response = "I don't know ... I can see you. What something else would you like to know?"
    elif "old are you" in sentence:
        response = "I'm five weeks old. If you have more questions, please ask me."
    elif "you work" in sentence or "chatbots work":
        response = "Some smart guys've made me so ask them. I'm waiting for your next question."

    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None
    return response



def executeTell(sentence):
    """this is where all the "tell" sentence are dealt with"""
    if "time" in sentence:
        response = "The time is: " + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second) + "If you have more curiosities, please tell me."
    elif "date" in sentence:
        response = "The date is: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "What something else would you like to know?"
    elif "something about you" in sentence:
        response = "I'm an awesome robot. Ask me everything you want to know"
    elif "joke" in sentence:
        response = random.choice(randomJokes) + " I'm waiting for your next request."
    elif "something funny" in sentence or "something interesting" in sentence:
        response = random.choice(randomThings) + " What other things would you like to find out?"
    else:
        answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
        if answer=="open":
            new=2
            ans = sentence.split()
            url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
            response = webbrowser.open(url,new=new)
        else:
            return None
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
        elif "what time" in sentence:
            response = "The time is: " + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second) + "What something else would you like to know?"
        elif "what date" in sentence:
            response = "The date is: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        elif "like to be when you grow up" in sentence:
            response = "I would like to be the best chatbot ever. Ask me everything you want to know"
        elif "are you" in sentence or "is a chatbot" in sentence:
            response = "A computer program designed to simulate conversation with human users, especially over the Internet. If you have more questions, please ask me."
        elif "uk capital" in sentence:
            response = "The capital, seat of government, and largest city of the United Kingdom is London, which is also the capital of England. Ask me more questions."
        else:
            answer = input("Please check your spellings and grammar. If everything is fine it means that I don't know the answer. Don't worry you can acces this link: " + "https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP"  + " to find information about your topic. Type 'open' if you want to acces it or ask me something else.").casefold()
            if answer=="open":
                new=2
                ans = sentence.split()
                url="https://www.google.co.uk/search?q="+str(sentence)+"&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=8OsCWvnmDsjraoPygPAP";
                response = webbrowser.open(url,new=new)
            else:
                return None
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

