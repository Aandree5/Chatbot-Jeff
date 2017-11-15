from pathlib import Path
import json

def famousbirthdays(fileName):
    with open('{}.sql'.format(fileName), "r", encoding = "utf-8") as sqlFile:
        with open('{}.json'.format(fileName), 'w') as outfile:
            readData = False
            try:
                for l in sqlFile:
                    if (l == "\n"):
                        continue
                    if (not readData and l.split(" ")[0] == "INSERT"):
                        readData = True
                    elif (readData):
                            noParentesis = l.replace("(" , "").replace("'),", "").replace("');", "")
                            noCommas = noParentesis.replace("', '", "#**#").replace(", '", "#**#")
                            line = noCommas.replace("\n", "").split("#**#")
                            
                            subData["Date"] = line[1]
                            subData["Name"] = line[2]
                            
                            Data.append(subData.copy())
            except:
                print("Error: Line {}".format(line[0]))
            json.dump(Data, outfile)
        

def mixedquotes(fileName):
    with open('{}.sql'.format(fileName), "r") as sqlFile:
        with open('{}.json'.format(fileName), 'w') as outfile:
            readData = False
            try:
                for l in sqlFile:
                    if (l == "\n"):
                        continue
                    if (not readData and l.split(" ")[0] == "INSERT"):
                        readData = True
                    elif (readData):
                            noParentesis = l.replace("(" , "").replace("'),", "").replace("');", "")
                            noCommas = noParentesis.replace("', '", "#**#").replace(", '", "#**#")
                            line = noCommas.replace("\n", "").split("#**#")
                            
                            nameList = line[1].split(", ")
                            rightName = " ".join(nameList[1:]) + " " + nameList[0]
    
                            subData["Name"] = rightName
                            subData["Type"] = line[2]
                            subData["Quote"] = line[3]
                            
                            Data.append(subData.copy())
            except:
                print("Error: Line {}".format(line[0]))
            json.dump(Data, outfile)


def todayinhistory(fileName):
    with open('{}.sql'.format(fileName), "r", encoding = "utf-8") as sqlFile:
        with open('{}.json'.format(fileName), 'w') as outfile:
            readData = False
            try:
                for l in sqlFile:
                    if (l == "\n"):
                        continue
                    if (not readData and l.split(" ")[0] == "INSERT"):
                        readData = True
                    elif (readData):
                            noParentesis = l.replace("(" , "").replace("'),", "").replace("');", "")
                            noCommas = noParentesis.replace("', '", "#**#").replace(", '", "#**#")
                            line = noCommas.replace("\n", "").split("#**#")
                            
                            subData["Date"] = line[1]
                            subData["Event"] = line[3]
                            
                            Data.append(subData.copy())
            except:
                print("Error: Line {}".format(line[0]))
            json.dump(Data, outfile)





nameOfFile = input("Name of SQL the File? ")

Data = []
subData = {}

if (nameOfFile == "famousbirthdays"):
    famousbirthdays(nameOfFile)
elif (nameOfFile == "mixedquotes"):
    mixedquotes(nameOfFile)
elif (nameOfFile == "todayinhistory"):
    todayinhistory(nameOfFile)


