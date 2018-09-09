import time
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse 
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
             "password" : input("Please introduce your password: "),
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
downloadPath = "D:\Alejandro\Downloads\Alud downloader test"

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
    tag["href"] = urllib.parse.urljoin(subjectURL, tag["href"])
    if os.path.splitext(os.path.basename(tag["href"]))[1] == ".pdf":
        tempFile = opener.open(tag["href"])
        print("Downloading %s", os.path.basename(tag["href"]))
        f = open(downloadPath + "\\" + os.path.basename(tag["href"], "wb"))
        f.write(current.read())
        f.close()
    
# UI end
print("Downloading completed!")
