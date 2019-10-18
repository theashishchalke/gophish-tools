from gophish import Gophish
from gophish.models import *
import urllib.request, json
import ssl
import re
import config

api_key = (config.api_key)
gohost = "GOPHISH_ADMINURL HERE"
campaignurl = "GOPHISH_CAMPAIGNURL_HERE"
api = Gophish(api_key, host=gohost, verify=False)

print("||||||||||WELCOME TO GoEmailReporter ||||||||")
print("\n********An EMAIL REPORTING TOOL for GOPHISH************")
print("#######By ASHISH CHALKE########\n")

#Get campaign Name
campaigndict = {} #Create an empty campaign dictionary
print("Printing a list of available campaigns:")
for campaign in api.campaigns.get(): #Use API Call to get all campaigns
    #Update campaigns to the campaigndict dictionary with campaignname:id format
    campaigndict.update([(campaign.name,str(campaign.id))])
    #Print all the available Campaigns.
    print("Name: " + campaign.name + " " + "ID: " + str(campaign.id))
#print(campaigndict) #Print the campaigndict dictionary for visual analysis

##THE ACTION to PULL the RID & make the request BEGINS!!!!
#Creating a while loop for exit condition
active = True
while active:
    #Let the user Select the campaign for RID
    askcampaign = input("\nEnter the name of the campaign: ")
    if re.search('\w+',askcampaign.lower()):
        print("\nThe campaign ID for the entered campaign is: "
            + campaigndict[askcampaign.title()])
        #Store the requested campaign in resultcampaign variable.
        resultcampaign = campaigndict[askcampaign.title()]
        #Get results for specific campaigns
        #Constructs URL to RESTAPI with campaign ID
        url = (gohost+"/api/campaigns/"+str(resultcampaign)+"/results?api_key="
              +api_key)
        #print(url) #Prints the URL. User for verification purposes only.
        #Bypasses SSL Verification
        context = ssl._create_unverified_context()
        #Requests the URL, Context bypasses ssl Verification
        campaignresponse = urllib.request.urlopen(url, context=context)
         #Parses the response via JSON in a campaigndata variable
        campaigndata = json.loads(campaignresponse.read())
        #Pulls the results for the campaign to a dictionary called \
        #campaignresults
        campaignresults = campaigndata['results']
        #print(bdata)
        #creates an empty dictionary for the RID to user mapping.
        riddict = {}
        #For Loop to parse individual items in list dict
        for campaignresult in campaignresults:
             #updates our empty dictionary
            riddict.update([(campaignresult['email'],campaignresult['id'])])
            #with the email and the rid of the user in email:rid format.
        #print(riddict) #Prints the RID Dictionary riddict list
        #Constructing the Report link:
        askemail = input("Enter the User's email address to report: ")
        if re.search('(.*)@(.*).(.*)',askemail.lower()):
            #We get the RID by comparing the email to the riddict dictionary.
            user_rid = riddict[askemail]
            #Tell the user the RID of the requested email address.
            print("RID for the User is: " + user_rid)
            #Ask the user if they want to verify on the user's behalf
            asktopost = input("Verify USER Reported Email? Type Y or N: ")
            #If yes
            if asktopost.title() == 'Y':
                #Construct the URL with the USER RID
                reporturl = campaignurl + "/report?rid=" + user_rid
                #Prints the URL for verification
                print("\nThis is the URL that will be opened: " + reporturl)
                #Open the url without SSL Verification and store the response in
                #report_response variable.
                report_response = urllib.request.urlopen(reporturl, \
                context=context)
                #Print the success and also the response if any.
                print("\nEmail Report updated for user" + askemail)
                print(report_response)
            #If not
            else:
                #Cancellation prompt
                print("Canceled on User input")
        else:
            active = False
            print("Please enter a valid email address.")
    else:
        active = False
        print("Please enter a correct campaign name.")
