from requests import request
import json
import sys

#Change these two with your onetimesecret.com email and API key
Username="" #Your onetimesecret email address EG: matt@example.com
APIKey="" #Your onetimesecret API key, EG: 68747470733a2f2f7777772e796f75747562652e636f6d2f77617463683f763d6451773477395767586351


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


###Main bit###
#Ask for secret
Secret=input("Enter secret string: ")

#Get timeout in secs, default is 3 days
TimeOut=input("Enter the secrets timeout in secs or press enter to default to 3 days: ")

if TimeOut.strip() == "":
    TimeOut="259200"
else:
    try:
        TimeOut=int(TimeOut)
    except:
        print("Error: Timeout value was not a number")
        exit()


#Create our URL
if APIOnline() == True:
    SecretJSON=CreateSecret(Secret,str(TimeOut))

    print(GenURL(SecretJSON["secret_key"]))
