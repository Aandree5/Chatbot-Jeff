# Gets JSON file data from a url
def readJSON(url):
    ''' Gets JSON file data from a url '''
    import urllib.request
    import json

    try:
        page = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        return("Error", 0)

    data = page.read()
    data.decode('utf-8')
    page.close()

    try:
        jsonData = json.loads(data)
    except:
        return("Error", 1)

    return(jsonData)

# If desn't exist, ask for a new token and save it on the file, if it does, then
# read it from the file
def tokenGetSet():
    ''' Gets the token from the file, or requests a new one, outputs the token '''
    from pathlib import Path

    if (Path("./data/token.jeff").exists()):
        with open('./data/token.jeff', "r") as tkFile:
            tkReq = tkFile.read()
        if (tkReq == "" or tkReq is None):
            return("Error", 7)
    else:
        tkReq = readJSON("https://opentdb.com/api_token.php?command=request")["token"]
        if ("Error" in tkReq):
            return(tkReq)
        
        Path('./data').mkdir(parents=True, exist_ok=True)
        with open('./data/token.jeff', "w") as tkFile:
            tkFile.write(tkReq)

    return(tkReq)

# Checks OpentDB categories and output them and the respective ID, if input true
# only output the categories names
def opentDBCat(onlyCategories = False):
    ''' Gets opentDB possibible categories and ID, if true just show the categories '''
    import html
    
    dbcat = readJSON('https://opentdb.com/api_category.php')
    if ("Error" in dbcat):
        return(dbcat)
    
    categories = []
    if (onlyCategories):
        for i in dbcat["trivia_categories"]:
            categories.append(html.unescape(i["name"].replace("Entertainment: ","")
                                                     .replace("Science: ", "")))
    else:
        for i in dbcat["trivia_categories"]:
            categories.append(html.unescape(i))
            
    return(categories)

# Gets questions from OpentDB, with defined criteria
def getOpentDB(category, difficulty, nrQuestions = 1):
    ''' With a set number of questions, category and difficulty level
        outputs the questions with that criteria '''
    import html
    import json

    ### Check if the number of questions is valid, more than 0 and less than 50
    if (nrQuestions is None or nrQuestions == ""
    or nrQuestions < 1 or nrQuestions > 50):
        return("Error" , 2)

    ### Get possible categories, check for validity and respective ID
    if (category != "" and category.casefold() != "Any".casefold()
    and category.casefold() != "Random".casefold()):
        cat = opentDBCat()
        catID = None
        for i in cat:
            if (category is not None and category != ""
            and category.casefold() in i["name"].casefold()):
                catID = "&category={}".format(i["id"])
                break
    
        if (catID == None):
            return("Error" , 3)
    else:
        catID = ""

    ### Check difficulty
    if (difficulty != "" and difficulty.casefold() != "Any".casefold()
    and difficulty.casefold() != "Random".casefold()):
        if (difficulty.casefold() in ["easy","medium","hard"]):
            diffID = "&difficulty={}".format(difficulty)
        else:
            return("Error" , 4)
    else:
        diffID = ""

    # Get token
    token = tokenGetSet()
    if ("Error" in token):
        return(token)
    else:
        tokenID = "&token={}".format(token)

    # Get JSON data from url with defined criteria   
    opentDBJson = readJSON(
        "https://opentdb.com/api.php?amount={}{}{}{}"
        .format(nrQuestions, catID, diffID, tokenID))
    if ("Error" in opentDBJson):
        return(opentDBJson)

    #Check website API response message
    if (opentDBJson["response_code"] == 0): #vSuccess - Read the data into variables
        if (nrQuestions == 1): #vIf just one question output string, if not, a list
            data = opentDBJson["results"][0]
            questions = html.unescape(data["question"])
            rightAns = html.unescape(data["correct_answer"])
            if (data["type"] == "boolean"):
                worngAns = html.unescape(data["incorrect_answers"][0])
            elif (data["type"] == "multiple"):
                worngAns = [html.unescape(data["incorrect_answers"][0]),
                            html.unescape(data["incorrect_answers"][1]),
                            html.unescape(data["incorrect_answers"][2])]
            else:
                worngAns = html.unescape(data["incorrect_answers"])
            qTypes = html.unescape(data["type"])
        else:
            questions = []
            rightAns = []
            worngAns = []
            qTypes = []
            for i in opentDBJson["results"]:
                questions.append(html.unescape(i["question"]))
                rightAns.append(html.unescape(i["correct_answer"]))

                if (i["type"] == "boolean"):
                    worngAns.append(html.unescape(i["incorrect_answers"][0]))
                elif (i["type"] == "multiple"):
                    worngAns.append([html.unescape(i["incorrect_answers"][0]),
                                     html.unescape(i["incorrect_answers"][1]),
                                     html.unescape(i["incorrect_answers"][2])])
                else:
                    worngAns.append(html.unescape(i["incorrect_answers"]))
                qTypes.append(html.unescape(i["type"]))            
    elif (opentDBJson["response_code"] == 1): #No Results
        return("Error", 5)
    elif (opentDBJson["response_code"] == 2): #Invalid Parameter
        return("Error", 6)
    elif (opentDBJson["response_code"] >= 3): #Token Not Found (3) and Token Empty (4)
        return("Error", 7)

    return(questions, rightAns, worngAns, qTypes)

# Main function to get questions, choose database and check for the error messages
def getQuestion(category, difficulty, nrQuestions = 1, database = "opentDB"):
    ''' With the input of category, diffculty, number of wustions and the database
        to get them from, output the question(s), answers and type '''
    if (database == "opentDB"):
        allData = getOpentDB(category, difficulty, nrQuestions)
        if ("Error" in allData):
            if (allData[1] == 0):
                return("Error", "There was an error opening the URL")
            elif (allData[1] == 1):
                return("Error", "Error reading JSON data")
            elif (allData[1] == 2):
                return("Error", "The number of questions requested not valid")
            elif (allData[1] == 3):
                return("Error", "Category not valid")
            elif (allData[1] == 4):
                return("Error", "Difficulty not valid")
            elif (allData[1] == 5):
                return("Error", "No results were found")
            elif (allData[1] == 6):
                return("Error", "Invalid parameter")
            elif (allData[1] == 7):
                import os

                print("Token not found or all available question were used")
                print("Reseting token...")
                os.remove("./data/token.jeff")
                allData = getOpentDB(category, difficulty, nrQuestions)
                if ("Error" in allData):
                    return("Error", "Token not found or all available question were used")
                else:
                    return(allData)
        else:
            return(allData)
    else:
        print("No more databases")
                    
    


#questData = getQuestion("game","", 1)
#if (questData == None or "Error" in questData):
#    print(questData[1])
#else:
#    questions, rightAnswers, wrongAnswers, qTypes = questData
#
#    for i in range(0, len(questions)):
#        print(" Q: {} \n A: {} \n W: {} \n T: {} \n\n"
#              .format(questions[i], rightAnswers[i], wrongAnswers[i], qTypes[i]))
#    print(" Q: {} \n A: {} \n W: {} \n T: {} \n\n"
#            .format(questions, rightAnswers, wrongAnswers, qTypes))
