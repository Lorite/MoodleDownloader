import time
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup

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

# CODE log in 1
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
else:
    print("Error logging in.")

# data input 1
# TODO change to input
downloadPath = "D:\Alejandro\Downloads\Alud downloader test"

# CODE choose subject



# UI end
print("Downloading completed!")
