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
    if (category is None):
        return("Error" , 3)        
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

# Testing area, test all funcions with possible inputs
if (__name__ == "__main__"):
    import json
    import os
    import time
    import html
    
    ########## Test readJSON function ##########
    print("#" * 50)
    print("# Checking readJSON function, read JSON from url")
    time_Start = time.perf_counter()
    test_Json = readJSON("https://opentdb.com/api.php?amount=1")
    # Test 1 - If JSON had the required fields
    test_Error = (False if ("response_code" in test_Json and
                            "results" in test_Json and
                            "category" in test_Json["results"][0] and
                            "correct_answer" in test_Json["results"][0] and
                            "difficulty" in test_Json["results"][0] and
                            "incorrect_answers" in test_Json["results"][0] and
                            "question" in test_Json["results"][0] and
                            "type" in test_Json["results"][0]) else True)

    print(" - Read JSON: {}".format("OK" if not test_Error else
                                    "NOT OK\n - JSON:\n{}".format(test_Json)))
    print("# Ran 1 test in {}s".format(round(time.perf_counter() - time_Start, 3)))

    ########## Test tokenGetSet function ##########
    print()    
    print("#" * 50)
    print("# Checking tokenGetSet function, get a token, store an read it")
    os.rename("./data/token.jeff", "./data/temp_tk.jeff")
    time_Start = time.perf_counter()
    # Test 1 - If token works on the website API
    test_Token = tokenGetSet()
    test_UseToken = readJSON("https://opentdb.com/api.php?amount=1&token={}"
                             .format(test_Token))
    test_Error = (False if (test_UseToken["response_code"] != 3) else True)
    print(" - Get token: {}".format("OK" if not test_Error else
                                    "NOT OK\n - TOKEN: {}".format(test_Token)))
    # Test 2 -  If token was kept in file, and if function reads it
    with open('./data/token.jeff', "r") as test_TkFile:
        test_tokenFile = test_TkFile.read()
    print(" - Read token: {}".format("OK" if test_Token == test_tokenFile
                                     else "NOT OK\n - TOKEN: {}".format(test_Token)))

    print("# Ran 2 tests in {}s".format(round(time.perf_counter() - time_Start, 3)))
    os.remove("./data/token.jeff")
    os.rename("./data/temp_tk.jeff", "./data/token.jeff")

    ########## Test opentDBCat function ##########
    print()  
    print("#" * 50)
    print("# Checking opentDBCat function, get possible categories")
    time_Start = time.perf_counter()
    test_categories = opentDBCat();
    # Test 1 - If categories has the required fields
    test_Error = (False if ("id" in test_categories[0] and
                           "name" in test_categories[0]) else True)
    print(" - Get Categories: {}".format("OK" if not test_Error else
                                         "NOT OK\nCATEGORIES:\n{}".format(test_categories)))
    # Test 2 - If function sorts only the categories
    test_temp_cat = []
    for i in test_categories:
        test_temp_cat.append(html.unescape(i["name"].replace("Entertainment: ","")
                                                    .replace("Science: ", "")))
    test_onlyCategories = opentDBCat(True);
    print(" - Only Categories: {}".format("OK" if (test_onlyCategories == test_temp_cat) else
                                          "NOT OK\nONLY CATEGORIES:\n{}".format(test_onlyCategories)))
    print("# Ran 2 tests in {}s".format(round(time.perf_counter() - time_Start, 3)))
    
    ########## Test getOpentDB function ##########
    print()
    print("#" * 50)
    print("# Checking getOpentDB function, get data from OpentDB")
    time_Start = time.perf_counter()
    # Test 1 - If function gets random data
    test_Data = getOpentDB("", "")
    test_Error = (False if (len(test_Data) == 4) else True)
    print(" - Random data: {}".format("OK" if not test_Error else
                                    "NOT OK\n - RANDOM:\n{}".format(test_Data)))
    # Test 2 - If function gets all categories
    test_Error = False
    test_catList = opentDBCat(True)
    test_catList.append(None)
    for i in test_catList:
        test_Data = getOpentDB(i, "")
        if (len(test_Data) != 4 and test_Data[1] != 3):
            test_Error = True
            test_Cat = test_Data
            break
    print(" - All Categories: {}".format("OK" if not test_Error else
                                       "NOT OK\n - CATEGORY:\n{}".format(test_Cat)))
    # Test 3 - If function gets all difficulties
    test_Error = False
    for i in ["easy", "medium", "hard", None]:
        test_Data = getOpentDB("", i)
        if (len(test_Data) != 4 and test_Data[1] != 4):
            test_Error = True
            test_Dif = test_Data
            break
    print(" - All Difficulties: {}".format("OK" if not test_Error else
                                       "NOT OK\n - DIFFICULTY:\n{}".format(test_Dif)))
    # Test 4 - If function possible number of questions Input
    test_Error = False
    test_nrQuest = [-50, -1, 0, 1, 50, None]
    for i in test_nrQuest:
        test_Data = getOpentDB("", "", i)
        if (len(test_Data) != 4 and test_Data[1] != 2):
            test_Error = True
            test_Ques = test_Data
            break
    print(" - Questions: {}".format("OK" if not test_Error else
                                    "NOT OK\n - QUESTIONS:\n{}".format(test_Ques)))
    print("# Ran 4 test in {}s".format(round(time.perf_counter() - time_Start, 3)))
