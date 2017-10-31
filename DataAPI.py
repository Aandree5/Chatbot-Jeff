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
        tkJSON = readJSON("https://opentdb.com/api_token.php?command=request")
        if ("Error" in tkJSON):
            return(tkJSON)
        tkReq = tkJSON["token"]
        Path('./data').mkdir(parents=True, exist_ok=True)
        with open('./data/token.jeff', "w") as tkFile:
            tkFile.write(tkReq)

    return(tkReq)

# Checks OpentDB categories and output them and the respective ID, if input true
# only output the categories names
def getCategories(onlyCategories = False, nrCat = 0):
    ''' Gets opentDB possibible categories and ID, if true just show the categories '''
    import html
    import random
    
    if (onlyCategories != False and onlyCategories !=  True):
        return("Error", 6)

    if (nrCat < 0):
        return("Error", 6)
    
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

    if (nrCat > 0 and nrCat < len(categories)):
        tempCat = categories
        categories = random.sample(tempCat, nrCat)
    
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
    if (category is None):
        return("Error" , 3)        
    if (category != "" and category.casefold() != "Any".casefold()
    and category.casefold() != "Random".casefold()):
        cat = getCategories()
        if ("Error" in cat):
            return(cat)
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
    if (difficulty is None):
        return("Error" , 4)   
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

    # Check website API response message
    if (opentDBJson["response_code"] == 0): # Success - Read the data into variables
        if (nrQuestions == 1): # If just one question output string, if not, a list
            data = opentDBJson["results"][0]
            questions = html.unescape(data["question"])
            rightAns = html.unescape(data["correct_answer"])
            if (data["type"] == "boolean"):
                worngAns = [html.unescape(data["incorrect_answers"][0])]
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
                    worngAns.append([html.unescape(i["incorrect_answers"][0])])
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
def getQuestion(category, difficulty, nrQuestions = 1):
    ''' Given a category, diffculty as strings and number
        of questions as integer return a dictionary with
        type, question, possible answers and correct answer '''
    import random

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

    ### Creates a dictionary with all the questios info, randomizes
    # the answers as a A, B, C, D multiple choice option, ouputs
    # a list of dictionaries if more than one questions is requested, also
    # appends the correct answer for later comparison
    if (nrQuestions == 1):
        questionSet = {}
        questionSet["Type"] = allData[3]
        questionSet["Question"] = allData[0]
        choices = (["A", "B", "C", "D"] if (allData[3] == "multiple")
                    else ["A", "B"])
        ansTemp = allData[2] 
        ansTemp.append(allData[1])
        random.shuffle(ansTemp)
        for i, item in enumerate(ansTemp):
            questionSet[choices[i]] = item
            if item == allData[1]:
                questionSet["corrAnswer"] = choices[i]
    else:
        questionSet = []
        for i in range(len(allData[2])):
            setTemp = {}
            setTemp["Type"] = allData[3][i]
            setTemp["Question"] = allData[0][i]
            choices = (["A", "B", "C", "D"] if (allData[3][i] == "multiple")
                                                else ["A", "B"])
            ansTemp = allData[2][i]
            ansTemp.append(allData[1][i])
            random.shuffle(ansTemp)   
            for a, item in enumerate(ansTemp):
                setTemp[choices[a]] = item
                if item == allData[1][i]:
                    setTemp["corrAnswer"] = choices[a]
            questionSet.append(setTemp)
                
    return(questionSet)

# Testing area, test all funcions with possible inputs
if (__name__ == "__main__"):
    import json
    import os
    import time
    import html
    from pathlib import Path
    
    ########## Test readJSON function ##########
    print("#" * 50)
    print("# Checking readJSON function, read JSON from url")
    time_Start = time.perf_counter()
    # Test 1 - If JSON had the required fields
    test_Json = readJSON("https://opentdb.com/api.php?amount=1")
    print(" - Read JSON: ", end="")
    
    test_Error = (False if ("response_code" in test_Json and
                            "results" in test_Json and
                            "category" in test_Json["results"][0] and
                            "correct_answer" in test_Json["results"][0] and
                            "difficulty" in test_Json["results"][0] and
                            "incorrect_answers" in test_Json["results"][0] and
                            "question" in test_Json["results"][0] and
                            "type" in test_Json["results"][0]) else True)

    print("OK" if not test_Error else "NOT OK\n{}".format(test_Json))
    print("# Ran 1 test in {}s".format(round(time.perf_counter() - time_Start, 3)))
    ########## Test tokenGetSet function ##########
    print()    
    print("#" * 50)
    print("# Checking tokenGetSet function, get a token, store an read it")
    if (Path("./data/token.jeff").exists()):
        os.rename("./data/token.jeff", "./data/temp_tk.jeff")
    time_Start = time.perf_counter()
    # Test 1 - If token works on the website API
    print(" - Get token: ", end="")
    
    test_Token = tokenGetSet()
    test_UseToken = readJSON("https://opentdb.com/api.php?amount=1&token={}"
                             .format(test_Token))
    test_Error = (False if ("Error" not in test_UseToken and
                            test_UseToken["response_code"] != 3) else True)
    
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Token))
    # Test 2 -  If token was kept in file, and if function reads it
    print(" - Read token: ", end="")
    
    test_tokenFile = "Error"
    if (Path("./data/token.jeff").exists()):
        with open('./data/token.jeff', "r") as test_TkFile:
            test_tokenFile = test_TkFile.read()
            
    print("OK" if test_Token == test_tokenFile else "NOT OK\n{}".format(test_Token))

    print("# Ran 2 tests in {}s".format(round(time.perf_counter() - time_Start, 3)))
    if (Path("./data/token.jeff").exists()):
        os.remove("./data/token.jeff")
    if (Path("./data/temp_tk.jeff").exists()):
        os.rename("./data/temp_tk.jeff", "./data/token.jeff")

    ########## Test getCategories function ##########
    print()  
    print("#" * 50)
    print("# Checking getCategories function, get possible categories")
    time_Start = time.perf_counter()
    # Test 1 - If categories has the required fields
    test_categories = getCategories();
    print(" - Get Categories: ", end="")
    
    test_Error = (False if ("id" in test_categories[0] and
                           "name" in test_categories[0]) else True)

    print("OK" if not test_Error else "NOT OK\n{}".format(test_categories))
    # Test 2 - If function sorts only the categories
    print(" - Only Categories: ", end="")
    
    test_temp_cat = []
    if ("Error" not in test_categories):
        for i in test_categories:
            test_temp_cat.append(html.unescape(i["name"]
                                               .replace("Entertainment: ","")
                                               .replace("Science: ", "")))
    test_onlyCategories = getCategories(True);
    
    print("OK" if (test_onlyCategories == test_temp_cat)
          else "NOT OK\n{}".format(test_onlyCategories))
    # Test 3 - If returns a set number of random categories
    test_nrCat = [-30, -24, -10, -1, 0, 1, 10, 24, 30]
    print(" - Rendom Categories: ", end="")

    for i in test_nrCat:
        test_randomCat = getCategories(True, i)
        test_Error = (False if (test_randomCat in test_onlyCategories or
                                test_randomCat == test_onlyCategories) else True)

    print("OK" if not test_Error else "NOT OK\n{}".format(test_randomCat))
    print("# Ran 2 tests in {}s".format(round(time.perf_counter() - time_Start, 3)))
    
    ########## Test getOpentDB function ##########
    print()
    print("#" * 50)
    print("# Checking getOpentDB function, get data from OpentDB")
    time_Start = time.perf_counter()
    # Test 1 - If function gets random data
    print(" - Random data: ", end="")
    
    test_Data = getOpentDB("", "")
    test_Error = (False if (len(test_Data) == 4) else True)
    
    print("{}".format("OK" if not test_Error else "NOT OK\n{}".format(test_Data)))
    # Test 2 - If function gets all possible categories
    print(" - All Categories: ", end="")
    
    test_Error = False
    test_catList = getCategories(True)
    if ("Error" in test_catList):
        test_Error = True
        test_Cat = test_catList
    else:
        for i in test_catList:
            test_Data = getOpentDB(i, "")
            if (len(test_Data) != 4 and test_Data[1] != 3):
                test_Error = True
                break
            
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    # Test 3 - If function gets all difficulties
    print(" - All Difficulties: ", end="")
    
    test_Error = False
    for i in ["easy", "medium", "hard"]:
        test_Data = getOpentDB("", i)
        if (len(test_Data) != 4 and test_Data[1] != 4):
            test_Error = True
            break
        
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    # Test 4 - If function possible number of questions Input
    print(" - Number Questions: ", end="")
    
    test_Error = False
    test_nrQuest = [-50, -1, 0, 1, 50]
    for i in test_nrQuest:
        test_Data = getOpentDB("", "", i)
        if (len(test_Data) != 4 and test_Data[1] != 2):
            test_Error = True
            break
        
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    print("# Ran 4 test in {}s".format(round(time.perf_counter() - time_Start, 3)))
    ########## Test getQuestion function ##########
    print()
    print("#" * 50)
    print("# Checking getQuestion function, format questions and check for errors")
    time_Start = time.perf_counter()
    # Test 1 - If function gets random data
    print(" - Random data: ", end="")
    
    test_Data = getQuestion("", "")
    test_Error = (False if ("Type" in test_Data and "Question" in test_Data and
                            "A" in test_Data and "B" in test_Data and
                            "corrAnswer" in test_Data) else True)
    
    print("{}".format("OK" if not test_Error else "NOT OK\n{}".format(test_Data)))
    # Test 2 - If function gets all possible categories
    print(" - All Categories: ", end="")
    
    test_Error = False
    test_catList = getCategories(True)
    if ("Error" in test_catList):
        test_Error = True
        test_Cat = test_catList
    else:
        for i in test_catList:
            test_Data = getQuestion(i, "")
            if ("Type" not in test_Data or "Question" not in test_Data or
                "A" not in test_Data or "B" not in test_Data or
                "corrAnswer" not in test_Data):
                test_Error = True
                break
            
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    # Test 3 - If function gets all difficulties
    print(" - All Difficulties: ", end="")
    
    test_Error = False
    for i in ["easy", "medium", "hard"]:
        test_Data = getQuestion("", i)
        if ("Type" not in test_Data or "Question" not in test_Data or
            "A" not in test_Data or "B" not in test_Data or
            "corrAnswer" not in test_Data):
            test_Error = True
            break
        
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    # Test 4 - If function possible number of questions Input
    print(" - Number Questions: ", end="")
    
    test_Error = False
    test_nrQuest = [-100, -50, -1, 0, 1, 50, 100]
    for i in test_nrQuest:
        test_Data = getQuestion("", "", i)
        
        if (i == 1):
            test_Error = (False if ("Type" in test_Data
                                    and "Question" in test_Data and
                                    "A" in test_Data and "B" in test_Data and
                                    "corrAnswer" in test_Data) else True)
        else:
            if (len(test_Data) != i and test_Data[0] != "Error"):
                test_Error = True
                break
            elif (test_Data[0] != "Error"):
                for i in test_Data:
                    test_Error = (False if ("Type" in i and "Question" in i and
                                            "A" in i and "B" in i and
                                            "corrAnswer" in i) else True)
        
    print("OK" if not test_Error else "NOT OK\n{}".format(test_Data))
    print("# Ran 4 test in {}s".format(round(time.perf_counter() - time_Start, 3)))
