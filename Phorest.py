import requests
import json
import sys
import operator

from requests.auth import HTTPBasicAuth

branchId = "SE-J0emUgQnya14mOGdQSw"

def FindClient():
    while 1:
        
        resp = requests.get('http://api-gateway-dev.phorest.com/third-party-api-server/api/business/eTC3QY5W3p_HmGHezKfxJw/client', auth=HTTPBasicAuth('global/cloud@apiexamples.com', 'VMlRo/eh+Xd8M~l'))
        if resp.status_code != 200:
    # This means something went wrong.
            print(resp.status_code)

        j = resp.json()
        clientList = j["_embedded"]["clients"]
        mobileList = sorted(clientList, key=operator.itemgetter('mobile'))
        emailList = sorted(clientList, key=operator.itemgetter('email'))
        
        print("Search for a client to create a voucher.")
        method = raw_input("Would you like to search by a) phone or b) email? Respond with 'a' or 'b'.")
        
        if method == "a":
            number = raw_input("Enter the phone number.")
            clientID = binarySearchNumber(mobileList, number)
    
        if method == "b":
            number = raw_input("Enter the email.")
            clientID = binarySearchEmail(emailList, number)
        
        if clientID == -1:
            print ("Client not found.")
                
        else:
            print "Client found. ID: " + clientID
            addVoucher(clientID)

def addVoucher(clientID):
    amount = raw_input("Enter the value of the voucher.")
    task = {
        "clientId": clientID,
            "creatingBranchId": branchId,
                "expiryDate": "2019-09-24T19:07:33.768Z",
                    "issueDate": "2018-09-24T19:07:33.768Z",
                        "links": [
                                  {
                                  "href": "string",
                                  "rel": "string",
                                  "templated": True
                                  }
                                  ],
                            "originalBalance": amount,
                                "remainingBalance": amount
    }
    
    resp3 = requests.post('http://api-gateway-dev.phorest.com/third-party-api-server/api/business/eTC3QY5W3p_HmGHezKfxJw/voucher', json=task, auth=HTTPBasicAuth('global/cloud@apiexamples.com', 'VMlRo/eh+Xd8M~l'))

    if resp3.status_code != 201:
        print(resp3.status_code)

    else:
        print("Voucher added.")

def binarySearchNumber(clients, number):
    first = 0
    last = len(clients)-1
    found = False
    ID = -1
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if clients[midpoint]["mobile"] == number:
            found = True
            ID = clients[midpoint]["clientId"]
        else:
            if number < clients[midpoint]["mobile"]:
                last = midpoint-1
            else:
                first = midpoint+1

    return ID

def binarySearchEmail(clients, email):
    first = 0
    last = len(clients)-1
    found = False
    ID = -1
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if clients[midpoint]["email"] == email:
            found = True
            ID = clients[midpoint]["clientId"]
        else:
            if email < clients[midpoint]["email"]:
                last = midpoint-1
            else:
                first = midpoint+1

    return ID

if __name__ == "__main__":
    
    sys.exit(FindClient())
