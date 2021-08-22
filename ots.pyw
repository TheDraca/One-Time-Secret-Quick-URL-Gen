from requests import request
import os
import json
import JsonControl

#Function to check API is ok
def APIOnline(Username,APIKey):
    try:
        Response = request("GET", "https://onetimesecret.com/api/v1/status", auth=(Username,APIKey))
        if "Not authorized" not in str(Response):  
            Status = Response.json()["status"]
            if Status == "nominal":
                return True
            else:
                return False
        else:
            print("Bad login details")
            exit()
    except:
        print("Unknown error when checking if API is online. Most likely incorrect login info")
        exit()


##First Time Setup function to get API details if not saved##
def FirstTimeSetup():
    print("This appears to be your first time running OTS, please provide API info")
    Username=input("Please enter your OTS email: ")
    APIKey=input("Please enter your API Key: ")

    #Check these  are correct
    if APIOnline(Username,APIKey) == True:
        try:
            JsonControl.SaveItem("API","Username",Username)
            JsonControl.SaveItem("API","Key",APIKey)
            print("API Username/Key confimed as correct and saved! Now running as normal \n")
        except:
            print("Unknown error writing API Username + Key, quitting")
            exit()
    else:
        print("Unable to verify the Username/API Key combo, quitting")
        exit()

        
    
#Check if we have our settings file and if its setup
if os.path.exists("OTS.json") == False:
    #Settings file does not exist, generating
    print("JSON File Missing, one has been genrated for you in the same directory as this script")
    JsonControl.GenJSONFile()
    FirstTimeSetup()
elif len(JsonControl.GetItem("API","Username")) <1 or len(JsonControl.GetItem("API","Key")) <1:
    FirstTimeSetup()

#Pull settings from out json file, if the config file is 
try:
    Username=JsonControl.GetItem("API","Username")
    APIKey=JsonControl.GetItem("API","Key")
    DefaultTimeOut=JsonControl.GetItem("Settings","DefaultTimeOut")
except KeyError:
    print("JSON File has not been configured yet")
    FirstTimeSetup()


#Build time factors directory
TimeUnitsFactors={"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800} #Directory to specfiy how to turn units into correct secs


def CreateSecret(Secret,TimeOut,Username=Username,APIKey=APIKey):
    try:
        payload= {
        'secret': Secret,
        'ttl': TimeOut
        }

        Response = request("POST", "https://onetimesecret.com/api/v1/share", auth=(Username,APIKey), data=payload)

        if Response.status_code == 200:
            return Response.json()
        else:
            print("Error talking to onetimesecret")
            exit()
    except:
        print("Unknown error while attempting to create secret")
        exit()

def GenURL(Secret_Key):
    URL="https://onetimesecret.com/secret/"
    URL=URL+Secret_Key
    return URL


#Function to turn user input into secs
def ConvertTimeToSecs(TimeOut):
    #Try seprate the input of units and numbers into their own values
    TimeOutUnit=TimeOut[-1].lower()  #Turn last part of inout into our unit
    if TimeOutUnit.isalpha() and TimeOutUnit in TimeUnitsFactors.keys(): #Check this is both a letter, and one of our keys in the TimeUnitsFactors dict
        TimeOutNum=TimeOut[:-1] #Get the rest of the string
        if TimeOutNum.isnumeric(): #Make sure the rest is a number
            TimeOutNum=int(TimeOutNum) #Turn that into an int for math later
        else:
            print("Invalid timeout length")
            exit()
    else:
        print("Incorrect unit of time")
        exit()
    TimeOutInSecs=TimeOutNum * TimeUnitsFactors[TimeOutUnit]

    return TimeOutInSecs


###Main bit###
#Ask for secret
Secret=input("Enter secret string: ")

#Check there is at least one character in the secret
if len(Secret) < 1:
    print("Empty secret provided, quitting")
    exit()

#Get timeout in secs, otherwise load the default at the top of the script
TimeOut=input("Enter the timeout for your secret in secs or press enter for {0}: ".format(DefaultTimeOut))

if TimeOut.strip() == "":
    TimeOut=ConvertTimeToSecs(DefaultTimeOut)
else:
    TimeOut=ConvertTimeToSecs(TimeOut)

#Create our URL
if APIOnline(Username,APIKey) == True:
    SecretJSON=CreateSecret(Secret,str(TimeOut))
    print("\nShare the link below:")
    print(GenURL(SecretJSON["secret_key"]))
