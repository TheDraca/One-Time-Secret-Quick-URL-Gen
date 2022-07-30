import json

def GenJSONFile(Filename="OTS.json"):
    with open(Filename, "w+") as JSONFile:
        FileContents={
            "API": {
                "URL": "",
                "Username" : "",
                "Key" : ""
            },
            "Settings": {
                "DefaultTimeOut": "3d"
            }
            }
        json.dump(FileContents,JSONFile)

def GetCurrentContents(Filename="OTS.json"):
    with open(Filename, "r") as JSONFile:
        return json.load(JSONFile)

def GetItem(ItemKey,ItemName,Filename="OTS.json"):
    with open(Filename, "r") as JSONFile:
        return (json.load(JSONFile)[ItemKey][ItemName])

def SaveItem(ItemKey, ItemName, Item, Filename="OTS.json"):
    Contents=GetCurrentContents(Filename)
    with open(Filename, "w+") as JSONFile:
        (Contents[ItemKey])[ItemName] = Item
        json.dump(Contents,JSONFile)
