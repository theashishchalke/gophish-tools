from gophish import Gophish
from gophish.models import *
import urllib.request, json
import ssl
import re
import config
import fileimport
import imaplib
import email
import io
import base64

#Required declarations
api_key = (config.api_key)
gohost = "GOPHISH_ADMINURL HERE"
campaignurl = "GOPHISH_CAMPAIGNURL_HERE"
api = Gophish(api_key, host=gohost, verify=False)
phishers = []
listReporters = []
uniqReporters = []

print("|"*10 + "WELCOME TO GoEmailReporter" +"|"*10)
print("\n********An EMAIL REPORTING TOOL for GOPHISH*******")
print("#######By ASHISH CHALKE#######\n")

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
        #ASKING THE USER A CHOICE - Import File or manually enter address.

        print("Please select the below options: \
        \na - Manually enter Users email address.\
        \nb - Import a file with email addresses \
        \nc - Connect to email account and pull.")
        inputchoice = input("\nEnter your choice: ")

        if inputchoice.lower() == "a":
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
                    #Open the url without SSL Verification and store the
                    # response in #report_response variable.
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
        #IF User selects to import from file.
        elif inputchoice.lower() == "b":
            #Enter name of the file to use. Should be in same directory.
            emailfile = input("Enter the filename.E.g. email.txt: ")
            #Uses the importemail function from fileimport, and sets the file
            fileimport.importEmail(emailfile)
            #creates a list with only unique addresses from the function
            uniqEmails = set(fileimport.listEmail)
            print("\nReport Requests will be made for below emails:\n")
            #For loop to create requests to Report RIDs
            for uniqEmail in uniqEmails:
                print("\n" + uniqEmail)
                uniq_rid = riddict[uniqEmail]
                print("RID for the User is: " + uniq_rid)
                #Construct the URL with the USER RID
                reporturl = campaignurl + "/report?rid=" + uniq_rid
                #Open the url without SSL Verification and store the
                # response in #report_response variable.
                report_response = urllib.request.urlopen(reporturl, \
                context=context)
                #Print the success and also the response if any.
                #print(report_response)
            print("\nEmail Report updated for the below user:")
            for printEmail in uniqEmails:
                print(printEmail)
            active=False
        elif inputchoice.lower() == "c":
            #This block of code automatically reads unread messages from
            #specified inbox based on the subject specified and extracts from
            #addresses and then proceeds to report the rid using extraction
            #technique. Messages whose emails are extracted will automatically
            #marked as SEEN to as not to be reported again when the tool is rerun
            print("Enter a subject to search at the prompt. The search can perform exact \
            matches as well as partial matches. However try to be as specific as possible.")
            subject_line = input("Enter the email subject: ")

            print("\nMailbox values will be imported from the config.py file in\
            this directory. If this function fails, please ensure that the \
            values entered in config.py are correct.\n \
            Values imported include Mail server address, username, password.")

            #Creates a connection to the mailbox
            imap = imaplib.IMAP4_SSL(config.emailhost)
            #Login info
            imap.login(config.emailuser, config.emailpassword)
            #Select inbox folder
            status, data = imap.select('INBOX')
            #Search emails with the specified subject and only if they are unread
            status, messages = imap.search(None, 'UNSEEN','SUBJECT',
            subject_line)
            #Adds response to a list called mess.
            mess = messages[0]
            #Splits single list to each digit.
            message_list = mess.split()
            #Fetches the emails and stores in list called mail
            for message in message_list:
                typ, mails = imap.fetch(message, '(RFC822)')
                #For loop to extract from addresses from the mails.
                for mail in mails:
                    if isinstance(mail, tuple):
                        #Decodes into UTF-8, required for Python 3
                        bmail = [x.decode('utf-8') for x in mail]
                        #Stores the message and makes searchable.
                        msg = email.message_from_string(bmail[1])
                        #Extracts the from address for the email.
                        varFrom = msg['from']
                        #Replaces the <> in the email address with emptynesssss
                        varFrom = varFrom.replace('<', '')
                        varFrom = varFrom.replace('>', '')

                        #Splits the varFrom list
                        phishers = varFrom.split()
                        #Below codeblock validates if the parameter is an email address \
                        #If it is an email address appends it to the list listReporters
                        for phish in phishers:
                            if(fileimport.validateEmail(phish)):
                                listReporters.append(phish)
            #Only imports unique addresses from the listReporters list.
            uniqReporters = set(listReporters)
            #For loop to create requests to Report RIDs
            for uniqReporter in uniqReporters:
                print("\n" + uniqReporter)
                uniq_rid = riddict[uniqReporter]
                print("RID for the User is: " + uniq_rid)
                #Construct the URL with the USER RID
                reporturl = campaignurl + "/report?rid=" + uniq_rid
                #Open the url without SSL Verification and store the
                # response in #report_response variable.
                report_response = urllib.request.urlopen(reporturl, \
                context=context)
                #Print the success and also the response if any.
                #print(report_response)
            print("\nEmail Report updated for the below user:")
            for printReporter in uniqReporters:
                print(printReporter)
            active=False
        else:
            active = False
            print("No correct options were selected.")
    else:
        active = False
        print("Please enter a correct campaign name.")
