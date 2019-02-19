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
    print("\nLogged in succesfully!")
    time.sleep(1)
    print("\nPlease choose a subject to download files from the list (1-n):")
else:
    print("\nError logging in.")

# code choose subject
mainPageLinks = logInResponseHTMLParsed.find_all('h3', {'class':"coursename"})
availableSubjectsNames = [];
availableSubjectsLinks = [];
for mainPageLink in mainPageLinks:
    mainPageLink = mainPageLink.find('a');
    mainPageLinkParsed = mainPageLink["href"];
    if 'course' in mainPageLinkParsed:
        availableSubjectsNames.append(mainPageLink.get_text().strip())
        availableSubjectsLinks.append(mainPageLinkParsed);

for index, subject in enumerate(availableSubjectsNames, start=1):
    print("%d. %s" % (index, subject))

# data input 1 select subject to extract files from
subjectIndex = -1
while subjectIndex < 0 or subjectIndex > len(availableSubjectsLinks) - 1:
    subjectIndex = int(input("Selection: ")) - 1
subjectName = availableSubjectsNames[subjectIndex]
subjectURL = availableSubjectsLinks[subjectIndex]

# data input 2
# TODO change to input
downloadPath = os.path.dirname(sys.argv[0])

# create folder for the subject
subjectPath = downloadPath + "\\" + subjectName
if not os.path.exists(subjectPath):
    os.makedirs(subjectPath)

# code download all files from selected subject
subjectResponse = opener.open(subjectURL, userDataEncoded)
subjectResponseHTML = subjectResponse.read()
subjectResponseHTMLParsed = BeautifulSoup(subjectResponseHTML, features="html.parser")
sectionLinks = subjectResponseHTMLParsed.find_all('li', role='region')
for index, section in enumerate(sectionLinks, start=1):
    filesLinks = section.find_all('a', href=True)
    sectionName = str(index) + ". " + section.find('a', href=True).get_text()
    print("\nSection " + sectionName + ":")
    sectionPath = subjectPath + "\\" + sectionName
    if not os.path.exists(sectionPath):
        os.makedirs(sectionPath)

    index2 = 1;
    for tag in filesLinks:
        fileLink = urllib.parse.urljoin(subjectURL, tag["href"])
        if "resource" in fileLink:
            tempFile = opener.open(fileLink)

            # set file name
            fileName = str(index2) + ". " + tag.find('span', {"class":"instancename"}).get_text()

            # remove special characters
            fileName = fileName.replace('<', ' ')
            fileName = fileName.replace('>', ' ')
            fileName = fileName.replace(':', ' ')
            fileName = fileName.replace('/', ' ')
            fileName = fileName.replace('\\', ' ')
            fileName = fileName.replace('|', ' ')
            fileName = fileName.replace('"', '')
            fileName = fileName.replace('?', ' ')
            fileName = fileName.replace('*', ' ')

            # remove the word 'Archivo' if exists
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
            elif 'text' in fileType:
                fileName += '.rtf'  
            elif 'page' in fileType:
                # TODO
                fileName += ''
            elif 'url' in fileType:
                # TODO better
                fileName += '.html'          

            # save file
            print("Downloading %s" % fileName)
            f = open(sectionPath + "\\" + fileName, "wb")
            f.write(tempFile.read())
            f.close()

            index2+=1
                    
# UI end
print("Downloading completed!")
