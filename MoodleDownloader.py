import time
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse 
import getpass
import os
import sys

# UI 0
print("Program made by Alejandro Lorite studying @ University of Deusto for his and everyone's convenience. :)")
time.sleep(2)
print("This program does not store your username or password, don't worry.")
time.sleep(1)

# TODO input URL (moodle / alud / other
url = "https://alud.deusto.es/login/index.php"

# data input 0
userData = { "username" : input("Please introduce your username: "),
             "password" : getpass.getpass("Please introduce your password: "),
             "rememberusername" : 0}
userDataEncoded = urllib.parse.urlencode(userData).encode("utf-8")

# UI 1a
print("Initializating.", end='\r')
time.sleep(0.2)

# code log in 1
cookies = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPRedirectHandler(),
    urllib.request.HTTPHandler(debuglevel=0),
    urllib.request.HTTPSHandler(debuglevel=0),
    urllib.request.HTTPCookieProcessor(cookies))

# UI 1b
print("Initializating..", end='\r')
time.sleep(0.2)

# CODE log in 2
logInResponse = opener.open(url, userDataEncoded)
logInResponseHTML = logInResponse.read()
logInResponseHTMLParsed = BeautifulSoup(logInResponseHTML, features="html.parser")

# UI 1c
print("Initializating...")
time.sleep(0.2)
if (logInResponseHTMLParsed.head.find("title").text == "ALUD"):
    print("Logged in succesfully!")
    time.sleep(1)
    print("Please choose a subject to download files from the list:")
else:
    print("Error logging in.")

# data input 1
# TODO change to input
downloadPath = "D:\Downloads\Alud downloader test"

# TODO code choose subject
subjectsLinks = logInResponseHTMLParsed.find_all('a', href=True)
#subjectsLinks = subjectsLinks.find(class_='coursebox*')
#for index, subjectsLink in enumerate(subjectsLinksItems, start=1):
#    print(index, subjectsLink.pre)

# TODO data input 2 select subject to extract files from
subject = input()
subjectURL = "https://alud.deusto.es/course/view.php?id=8915"

# code download all files from selected subject
subjectResponse = opener.open(subjectURL, userDataEncoded)
subjectResponseHTML = subjectResponse.read()
subjectResponseHTMLParsed = BeautifulSoup(subjectResponseHTML, features="html.parser")
filesLinks = subjectResponseHTMLParsed.find_all('a', href=True)
for tag in filesLinks:
    fileLink = urllib.parse.urljoin(subjectURL, tag["href"])
    print("+++++++++++++")
    print(fileLink)
    print("-")
    print("--")
    if "resource" in fileLink:
        tempFile = opener.open(fileLink)

        # set file name
        fileName = tag.find('span', {"class":"instancename"}).get_text()
        if fileName.endswith(' Archivo'):
            fileName = fileName[:-8]
        fileType = tag.find('img', src=True)['src']
        if 'document' in fileType:
            fileName += '.docx'
        elif 'pdf' in fileType:
            fileName += '.pdf'
        elif 'powerpoint' in fileType:
            fileName += '.pptx'
        elif 'spreadsheet' in fileType:
            fileName += '.xlsx'
        elif 'archive' in fileType:
            fileName += '.rar'
        elif 'jpeg' in fileType:
            fileName += '.jpg'
        elif 'bmp' in fileType:
            fileName += '.bmp'
        elif 'png' in fileType:
            fileName += '.png'
        elif 'page' in fileType:
            # TODO
        elif 'url' in fileType:
            # TODO better
            fileName += '.html'
                

        # save file
        print("Downloading %s" % fileName)
        f = open(downloadPath + "\\" + fileName, "wb")
        f.write(tempFile.read())
        f.close()
        break;
    
# UI end
print("Downloading completed!")
