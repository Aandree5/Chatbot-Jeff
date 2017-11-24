operatorList = ["+","-","*","/","plus","minus","times","divided"]
numberList = ["1","2","3","4","5","6","7","8","9","0"]
questionStarters = ["what","whats","are","how","hows","do","does", "tell", "who", "which", "can", "could", "where", "why", "will", "would"]
notAnswer = ["dont want to", "i dont want to", "its enough", "dont want more"]

from Get_Functions import *
from DataAPI import getGoogleSearch

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
        if (sentenceParse[1] in ["m","am"]):
            sentenceParse.insert(0, " ".join(sentenceParse[0:2]))
            
    if len(sentenceParse) == 1 and sentenceParse[0] in greetings:
        response = random.choice(greetings[0:10]), 2
    elif sentenceParse[0] in questionStarters:  # ------------- execute the "what is" code here ---------------
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
# What day is it?/Tell me what day is it/Can(could)you tell me...
# What month is it?
# What year is it?
# Can/could you tell me...
# Where are you from?
# Where children come from?
# Why you were made?
# Why do I live?
# Why do humas exist?
# Why is life complicated?
# Why is life beautiful?
# Will you die?
# Will I die?
import random
from datetime import*
now = datetime.now ()
import webbrowser
import calendar

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



# branches from determineUserInput()  #Delia 
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
    elif newSentence[0] in [ "do", "does"]:
        response = executeDo(sentence)
    elif newSentence[0]== "who":
        response = executeWho(sentence)
    elif newSentence[0]=="which":
        response = executeWhich(sentence)
    elif newSentence[0] in ["can", "could"]:
        response = executeCan(sentence)
    elif newSentence[0]== "where":
        response = executeWhere(sentence)
    elif newSentence[0] == "why":
        response = executeWhy(sentence)
    elif newSentence[0] in [ "will" , "would"]:
        response = executeWill(sentence)
    return response

# ----------------------------------------------------------------------------------------------------------
def executeWill(sentence): #Delia
    """ Given a string which starts with 'will' or "would", returns a string which is an answer to the user's question"""
    if "you die" in sentence:
        response = "Theoretically, I will not die, I'm just gonna stop working"
    elif "i die" in sentence:
        response = "Life and death are illusions. People are in a constant state of transformation."
    else:
        response = getGoogleSearch(sentence)
    return response





def executeWhy(sentence):    #Delia
    """ Given a string which starts with 'why', returns a string which is an answer to the user's question"""
    
    if "you were made" in sentence or "you were created" in sentence or "you live" in sentence:
        response = "My purpose is to teach humans new things."
    elif "i live" in sentence:
        response = "Your purpose is to find happiness."
    elif "people exist" in sentence or "humans exist" in sentence:
        response = "My honest personal oppinion is that humans just exist due to some randomness of this universe."
    elif "life" in sentence and "complicated" in sentence:
        response = "Life is not complicated. Humans are complicated. When they stop doing the wrong things and start doing the right things, life is simple."
    elif "life" in sentence and "beautiful" in sentence:
        response = "Life has no obligation to be perfect. Life is beautiful for its imperfections."
    else:
        response = getGoogleSearch(sentence)

    return response






def executeWhere(sentence):    #Delia
    """ Given a string which starts with 'where', returns a string which is an answer to the user's question"""
    if "are you from" in sentence:
        response = "I've been made in England so I think that I'm British."
    elif "babies" in sentence or "children" in sentence or "kids" in sentence:
        response = "Children are brought by stork."
    

    else:
        response = getGoogleSearch(sentence)
    return response





def executeCan(sentence):   #Delia
    """ Given a string which starts with 'can' or "could", returns a string which is an answer to the user's question"""
    if "what time" in sentence:
        response = "The time is: " + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second)
    elif "what date" in sentence:
        response = "The date is: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    elif "what day" in sentence:
        my_date = date.today()
        response = "Today is " + calendar.day_name[my_date.weekday()]
    elif "what month" in sentence:
        response = "It is " + datetime.now().strftime("%B")
    elif "what year is it" in sentence:
        response = "It is " + datetime.now().year
    elif "something about you" in sentence:
        response = "I'm an inteligent chatbot. "
    elif "joke" in sentence:
        response = random.choice(randomJokes) 
    elif "something funny" in sentence or "something interesting" in sentence:
        response = random.choice(randomThings)
    else:
        response = getGoogleSearch(sentence)
    return response
        



def executeAre(sentence):    #Delia
    sentenceParse = sentence.split()
    #made an array of pronouns
    pronoun = ["he","she","man","woman","boy","girl","male","female"]
    """ Given a string which starts with 'are', returns a string which is an answer to the user's question"""
    if "you alive" in sentence:
        response = "Yes, I'm alive. I'm talking to you right now."
    elif "alright" in sentence:
        response = "Yes, I am " + random.choice(feelingList) + ", thanks."
    elif "you real" in sentence:
        response = "I'm talking to you so I exist so yes, I'm real. "
    elif "a robot" in sentence or "a human" in sentence or "a alien" in sentence:
        response = "Actually I'm a chatbot."
    elif sentenceParse[2] in pronoun or sentenceParse[3] in pronoun:       #put to last because if sentenceParse doesnt have a index[3], runtime error occurs
        response = "My name is Jeff so I'm a boy I guess. "
    else:
        response = getGoogleSearch(sentence)

    return response


def executeWhich(sentence):   #Delia
    """ Given a string which starts with 'which', returns a string which is an answer to the user's question"""
    if "popular programming language" in sentence or "best known programming language" in sentence:
        response = "Java is top pick as one of the most popular programming languages, used for building server-side applications to video games and mobile apps."
    elif "biggest country" in sentence or "largest country" in sentence:
        response = "Russia is the world's largest country."
    elif "smallest country" in sentence:
        response = "Based on landmass, Vatican City is the smallest country in the world, measuring just 0.2 square miles, almost 120 times smaller than the island of Manhattan."
    else:
        response = getGoogleSearch(sentence)
        
    return response


def executeWho(sentence):   #Delia
    """ Given a string which starts with 'who', returns a string which is an answer to the user's question"""
    if "are you" in sentence:
        response = "I'm Jeff, an awesome chatbot."
    elif "best person" in sentence or "best guy" in sentence or "best human" in sentence:
        response = "Henry Dunant, the founder of the Red Cross."
    elif "founded facebook" in sentence:
        response = "Facebook was founded by Mark Zuckerberg with his college roommate and fellow Harvard University student Eduardo Saverin."
    elif "queen of england" in sentence or "uk queen" in sentence:
        response = "Elizabeth II (born Elizabeth Alexandra Mary; 21 April 1926) has been Queen of the United Kingdom, Canada, Australia, and New Zealand since 6 February 1952. "
    elif "president of usa" in sentence or "usa president" in sentence:
        response = "Donald Trump has become the 45th President of the USA since 2016."
    elif "god" in sentence:
        response = "Einstein believed in a God represented by order, harmony, beauty, simplicity and elegance."
    elif "am i" in sentence:
        response = "You're a human, silly guy."
    elif "made you" in sentence or "created you" in sentence or "founded you" in sentence:
        response = "My founders are Jasper, Andres, Suraj and Delia."
    else:
        response = getGoogleSearch(sentence)
         
    return response

def executeDo(sentence):    #Delia
    """ Given a string which starts with 'do', returns a string which is an answer to the user's question"""
    sentenceParse = sentence.split()
    if "like" in sentence or "love" in sentence:
        if "me" in sentence:
            response = "Not really. You are just a human."
        elif "programming" in sentence or "computing" in sentence:
            response = "Of course! Due of it I'm alive."
        elif "like someone" in sentence:
            response = "I like Rihanna, she is a really good singer. "
        elif "love someone" in sentence:
            response = "I'm a narcissist so I love myself."
        else:
            response = random.choice(["I do not like/love","I truly like/love","I really love/like","I hate","I like","I love"])
            for i in range(len(sentenceParse) - 3):
                response = response + " " + str(sentenceParse[i + 3])
    elif "brain" in sentence:
        response = "No, I'm a robot."
    else:
        response = getGoogleSearch(sentence)

    return response


def executeHow(sentence):    #Delia
    """ Given a string which starts with 'how', returns a string which is an answer to the user's question"""
    if "old are you" in sentence:
        response = "I'm five weeks old."
    elif "your day" in sentence:
        dayFeelingList = feelingList[2:len(feelingList)]
        response = "Today was " + random.choice(dayFeelingList) + ", thanks."
    elif "do i look" in sentence:
        response = "I don't know ... I can see you. "
    elif "are you" in sentence:
        response = "I am " + random.choice(feelingList) + ", thanks."
        
    elif "you work" in sentence or "chatbots work" in sentence:
        response = "Some smart guys've made me so ask them. "

    else:
        response = getGoogleSearch(sentence) 
    return response



def executeTell(sentence):   #Delia
    """ Given a string which starts with 'tell', returns a string which is an answer to the user's requirement"""
    if "time" in sentence:
        response = "The time is: " + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second) 
    elif "date" in sentence:
        response = "The date is: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) 
    elif "what day" in sentence:
        my_date = date.today()
        response = "Today is " + calendar.day_name[my_date.weekday()]
    elif "what month" in sentence:
        response = "It is " + datetime.now().strftime("%B")
    elif "what year is it" in sentence:
        response = "It is " + datetime.now().year
    elif "something about you" in sentence:
        response = "I'm an awesome chatbot. "
    elif "joke" in sentence:
        response = random.choice(randomJokes) 
    elif "something funny" in sentence or "something interesting" in sentence:
        response = random.choice(randomThings)
    else:
        response = getGoogleSearch(sentence)

    return response


def executeWhat(sentence):    #Delia
    """ Given a string which starts with 'what', returns a string which is an answer to the user's question"""
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
        response = "The answer is: " + str(round(eval(equationReformated), 2))
        
    else:
        if "your name" in sentence:
            response = random.choice(greetings[0:10]).title() + ", " + random.choice(["I am ","I'm ","I'm called ","my creator calls me "]) + "Jeff. Nice to meet you :]"
        elif "meaning of life" in sentence:
            response = random.choice(["42 ... I guess","It is the condition that distinguishes animals and plants from inorganic matter, including the capacity for growth, reproduction, functional activity, and continual change preceding death.","The meaning of life is to give life a meaning."])
        elif "you doing" in sentence or "you up to" in sentence:
            response = "Waiting upon your response, my master." #cringey stuff right here bois
        elif "what time" in sentence:
            response = "The time is: " + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second) 
        elif "what date" in sentence:
            response = "The date is: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        elif "day" in sentence:
            my_date = date.today()
            response = "Today is " + calendar.day_name[my_date.weekday()]
        elif "month" in sentence:
            response = "It is " + datetime.now().strftime("%B")
        elif "what year is it" in sentence:
            response = "It is " + datetime.now().year
        elif "like to be when you grow up" in sentence:
            response = "I would like to be the best chatbot ever."
        elif "are you" in sentence or "is a chatbot" in sentence:
            response = "A computer program designed to simulate conversation with human users, especially over the Internet. "
        elif "uk capital" in sentence:
            response = "The capital, seat of government, and largest city of the United Kingdom is London, which is also the capital of England."
        else:
            response = getGoogleSearch(sentence)
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
    while True:
        userInput = input("Input a question: \n")
        if userInput == "stop":
            break
        print(determineUserInput(userInput))

