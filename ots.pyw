from requests import request
import json

#Change these two with your onetimesecret.com email and API key
Username="" #Your onetimesecret email address EG: matt@example.com
APIKey="" #Your onetimesecret API key, EG: 68747470733a2f2f7777772e796f75747562652e636f6d2f77617463683f763d6451773477395767586351
DefaultTimeOut="3d" #Default time out in secs if the users just hits enter on the prompt
TimeUnitsFactors={"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800} #Directory to specfiy how to turn units into correct secs


#Function to check API is ok
def APIOnline(Username=Username,APIKey=APIKey):
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
        print("Unknown error when checking if API is online")
        exit()

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
if APIOnline() == True:
    SecretJSON=CreateSecret(Secret,str(TimeOut))
    print("\nShare the link below:")
    print(GenURL(SecretJSON["secret_key"]))
