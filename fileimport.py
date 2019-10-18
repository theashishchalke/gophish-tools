import re
#Credits to original code: csestack.org/python-extract-emails-read-file/


def validateEmail(strEmail):
    # .* Zero or more characters of any type.
    if re.match("(.*)@(.*).(.*)", strEmail):
        return True
    return False


listEmail = []
uniqEmails = []
def importEmail(fileToRead):
    delimiterInFile = [',', ';']
    file = open(fileToRead, 'r')
    listLine = file.readlines()
    for itemLine in listLine:
        item =str(itemLine)
        for delimeter in delimiterInFile:
            item = item.replace(str(delimeter),' ')

        wordList = item.split()
        for word in wordList:
            if(validateEmail(word)):
                listEmail.append(word)

    if listEmail:
        uniqEmails = set(listEmail)
        print(len(uniqEmails),"unique emails collected!")
    else:
        print("No email found.")
