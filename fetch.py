### Charlie Floquet CCC-410 Capstone Project
### April 2021
### BrickLink Interaction API 
### Requisite Files:
#  - auth.json (see GitHub for formatting instructions)


from bricklink_api.auth import oauth
print("[+] Imported OAuth from BrickLink API.")
from bricklink_api.catalog_item import get_price_guide, Type, NewOrUsed
print("[+] Imported Price Fetch Module from BrickLink API..")
import json
print("[+] Imported JSON...")
import os
# fill in with your data from https://www.bricklink.com/v2/api/register_consumer.page

def manualSelection():
    ## Retrieve important contextual information from user
    loop = True
    while loop is True:
        print("[  Welcome to BrickLink API Interactive Console:         ]")
        print("[  Which class of item would you like to search for?     ]")
        print("[                                                        ]")
        print("[      1. Parts/Pieces (1)                               ]")
        print("[      2. Minifigure (2)                                 ]")
        print("[      3. Complete Sets (3)                              ]")
        print("[                                                        ]")

        userChoice = input('')

        if userChoice == "1":
            print("[+] Parts/Pieces Selected.")
            loop = False
            classType = "PART"
        elif userChoice == "2":
            print("[+] Minifigures Selected.")
            loop = False
            itemType = "MINIFIG"
        elif userChoice == "3": 
            print("[+] Complete Sets Selected.")
            loop = False
            itemType="SET"
        else:
            print("[-] Sorry, that wasn't one of the options (1-3). Try again.")
            loop = True

# main will hold all of our other functions and run them
# runType is whether we want to run this program automatically or manually. 
def main(runType):
    ######## READ EXTERNAL DATA ##########
    #open the externally saved and defined credentials file for readings
    data = open("bricklink_api/auth.json", "r")
    authData = data.read()
    creds = json.loads(authData)
    #fetch credential data from dictionary
    consumer_key = creds['ConsumerKey']
    consumer_secret = creds['ConsumerSecret']
    token_value = creds['TokenValue']
    token_secret = creds['TokenSecret']

    ######## Define OAuth Authentication Using Imported Values #######
    auth = oauth(consumer_key, consumer_secret, token_value, token_secret) 
    selection = runType[0]
    if selection=="m" or selection=="M":
        print("[+] Manual Interaction Selected.")
        manualSelection()
    if selection=="a" or selection=="A":
        print("[+] Automated Interaction Selected.")
        id = runType[1]
        itemType = runType[2]
        avg_price = fetch(auth,id,itemType)
    return avg_price
def fetch(auth,id,itemType):
    # get price guide for a used 42100-1 (Lego Technic Liebherr R 9800)
    json_obj = get_price_guide(itemType, id, new_or_used=NewOrUsed.USED, auth=auth)

    avg_price = json_obj.get('data').get('avg_price')

    print("Six Month Average Selling Price: $",avg_price)
    return avg_price

runType = ["a", "sw0417", "MINIFIG"]
print("Welcome to Capstone BrickLink Interaction API! ")
avg_price = main(runType)
