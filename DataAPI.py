def readJSON(url):
    ''' Gets the data from a JSON url '''
    import urllib.request
    import json

    try:
        page = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("There was an error opening the URL (description below).")
        print(e)
        return(None)

    data = page.read()
    data.decode('utf-8')
    page.close()

    try:
        jsonData = json.loads(data)
    except:
        print("Error reading JSON data")
        return(None)

    return(jsonData)

def tokenGetSet():
    ''' Gets the token from the file, or requests a new one, outputs the token '''
    from pathlib import Path

    if (Path("./data/token.jeff").exists()):
        with open('./data/token.jeff', "r") as tkFile:
            tk = tkFile.read()
    else:
        tk = readJSON("https://opentdb.com/api_token.php?command=request")["token"]
        if (tk == None):
            print("Could not request token")
            return(None)
        
        Path('./data').mkdir(parents=True, exist_ok=True)
        with open('./data/token.jeff', "w") as tkFile:
            tkFile.write(tk)

    return(tk)

def openDBCats(onlyCategories = False):
    ''' Gets openDB possibible categories and ID, if true just show the categories '''
    import html
    dbcats = readJSON('https://opentdb.com/api_category.php')
    if (dbcats == None):
        print("Error getting categories")
        return(None)
    cats = []
    if (onlyCategories):
        for i in dbcats["trivia_categories"]:
            cats.append(html.unescape(i["name"].replace("Entertainment: ","")
                                               .replace("Science: ", "")))
    else:
        for i in dbcats["trivia_categories"]:
            cats.append(html.unescape(i))
    return(cats)
    

def getOpenDB(category, difficulty, nrQuestions = 1):
    ''' With a set number of questions, category and difficulty level
        outputs the questions with that criteria '''
    import html
    import json

    ### Check if the number of questions is valid, more than 0 and less than 50
    if (nrQuestions is None or nrQuestions == ""
        or nrQuestions < 1 or nrQuestions > 50):
        print("The number of questions requested its not valid.")
        return(None)

    ### Get possible categories, check for validity and respective ID
    cats = openDBCats()
    catID = None
    for i in cats:
        if (category is not None and category != ""
            and category.lower() in i["name"].lower()):
            catID = i["id"]
            break
    
    if (catID == None):
        print("Category not valid")
        return(None)

    ### Check difficulty
    if (difficulty is None or difficulty == ""
        or difficulty.lower() not in ["easy","medium","hard"]):
        print("Difficulty not valid")
        return(None)

    # Get token
    token = tokenGetSet()
    if (token == None):
        print("Could not get token")
        return(None)

    # Get JSON data from url with defined criteria
    openDBJson = readJSON(
        "https://opentdb.com/api.php?amount={}&category={}&difficulty={}&token={}"
        .format(nrQuestions, catID, difficulty, token))
    if (openDBJson == None):
        print("Could not get JSON data.")
        return(None)

    #Check website response message
    if (openDBJson["response_code"] == 0): #Success - Read the data into variables
        if (nrQuestions == 1):
            data = openDBJson["results"][0]
            questions = html.unescape(data["question"])
            rightAns = html.unescape(data["correct_answer"])
            if (data["type"] == "boolean"):
                worngAns = worngAns.append(html.unescape(data["incorrect_answers"]))
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
            for i in openDBJson["results"]:
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
    elif (openDBJson["response_code"] == 1): #No Results
        print("No results were found")
        return(None)
    elif (openDBJson["response_code"] == 2): #Invalid Parameter
        print("Invalid parameter")
        return(None)
    elif (openDBJson["response_code"] >= 3): #Token Not Found (3) and Token Empty (4)
        import os
        print("Token not found or all available question were used, reseting token.")
        os.remove("./data/token.jeff")
        return(None)

    return(questions, rightAns, worngAns, qTypes)


#allData = getOpenDB("Music","hard")
#if (allData is None):
#    print("Data is none, an error as occurred")
#    exit()
#else:
#    questions, rightAnswers, wrongAnswers, qTypes = allData
#    for i in range(0, len(questions)):
#        print(" Q: {} \n A: {} \n W: {} \n T: {} \n\n"
#              .format(questions[i], rightAnswers[i], wrongAnswers[i], qTypes[i]))
#    print(" Q: {} \n A: {} \n W: {} \n T: {} \n\n"
#              .format(questions, rightAnswers, wrongAnswers, qTypes))
