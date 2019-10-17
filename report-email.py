from gophish import Gophish
from gophish.models import *
import urllib.request, json
import ssl

api_key = 'b39cbc6caa750c7eeacbb82f76b50965be32837e8f8d1ffc9a6d5665a4a1fc79'
api = Gophish(api_key, host='https://10.70.70.15:3333', verify=False)

#Get campaign Name

campaigndict = {} #Create an empty campaign dictionary
print("Printing a list of available campaigns:")
for campaign in api.campaigns.get(): #Use API Call to get all campaigns
    #Update campaigns to the campaigndict dictionary with campaignname:id format
    campaigndict.update([(campaign.name,str(campaign.id))])
    #Print all the available Campaigns.
    print("Name: " + campaign.name + " " + "ID: " + str(campaign.id))
#print(campaigndict) #Print the campaigndict dictionary for visual analysis

#Let the user Select the campaign for RID
askcampaign = input("\nEnter the name of the campaign: ")
print("\nThe campaign ID for the entered campaign is: " + campaigndict[askcampaign.title()])

#Store the requested campaign in resultcampaign variable.
resultcampaign = campaigndict[askcampaign.title()]

#Get results for specific campaigns

url = "https://10.70.70.15:3333/api/campaigns/"+ str(resultcampaign) +"/results?api_key="+api_key  #Constructs URL to RESTAPI with campaign ID
#print(url) #Prints the URL. User for verification purposes only.
context = ssl._create_unverified_context() #Bypasses SSL Verification
campaignresponse = urllib.request.urlopen(url, context=context) #Requests the URL, Context bypasses ssl Verification
campaigndata = json.loads(campaignresponse.read()) #Parses the response via JSON in a campaigndata variable
campaignresults = campaigndata['results'] #Pulls the results for the campaign to a dictionary called campaignresults
#print(bdata)
riddict = {} #creates an empty dictionary for the RID to user mapping.
for campaignresult in campaignresults: #For Loop to parse individual items in list dict
    riddict.update([(campaignresult['email'],campaignresult['id'])]) #updates our empty dictionary
    #with the email and the rid of the user in email:rid format.
#print(riddict) #Prints the RID Dictionary riddict list

#Constructing the Report link:
askemail = input("Enter the email address of the user whose RID is required: ")
#We get the RID by comparing the email to the riddict dictionary.
user_rid = riddict[askemail]
#Tell the user the RID of the requested email address.
print("RID for the User is: " + user_rid)
#Ask the user if they want to verify on the user's behalf
asktopost = input("Verify USER Reported Email? Type Y or N: ")
campaignurl = "http://10.70.70.15"
#If yes
if asktopost == 'Y':
    #Construct the URL with the USER RID
    reporturl = campaignurl + "/report?rid=" + user_rid
    print("\nThis is the URL that will be opened: " + reporturl) #Prints the URL for verification
    #Open the url without SSL Verification and store the response in report_response variable.
    report_response = urllib.request.urlopen(reporturl, context=context)
    #Print the success and also the response if any.
    print("\nEmail Report updated for user" + askemail)
    print(report_response)
#If no
else:
    #Cancelleation prompt
    print("Canceled on User input")
