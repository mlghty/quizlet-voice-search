import win32clipboard,time
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import re,csv
import os,time
from gtts import gTTS
from googleapiclient.discovery import build
import json

language = 'en'




f = open('token.json')
data = json.load(f)
    
key = data['key'][0]
token = data['token'][0]

# print(key)
# print(token)
    

# quizzard
# C:\Users\vvarf\AppData\Local\Google\Chrome\User Data\Default\Extensions\oidgiplmcfbadgmofhjicgonldhkbooe

# row[0] == questions
# row[1] == answers


questions = open('Exam1.csv')
questions = csv.reader(open('Exam1.csv', "r"), delimiter=",")

error = 0
def getAnswer(pageUrl,question):
    global error
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
    'referer':'https://www.google.com/'
    }

    page = requests.get(str(pageUrl),headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find(class_="UIHeading UIHeading--one").text
    print("Page title: ",title)
    print("Searching for:", question)
    print("Page URL: ", pageUrl)

    time.sleep(3)
    
    try:
        print("in try")
        question1 = question
        print("Question in try: ", question1)
        title = soup.find(class_="UIHeading UIHeading--one").text

        a = re.compile(question1, flags=re.I)
        print("Re string: ", a.pattern)

        questionText = soup.find(string=a.pattern)
        # questionText = soup.find(a.pattern)
        questionText =soup.find(string=re.compile(question, flags=re.I))
        print("Question text: ", questionText)

        termList = soup.find(class_='SetPageTerm')
        # print("Term list: ", termList)

        # answerList = termList.find_all('SetPageTerm-wordText')
        # print("Answer list: ", answerList)

        # fails right below here at termWhole
        termWhole = questionText.parent.parent.parent.parent.parent
        # print("Term whole: ",termWhole)

        answerGroup = termWhole.find(class_='SetPageTerm-definitionText')
        # answerGroup = termWhole.find(class_='SetPageTerm-wordText')
        print("Answer Group: ", answerGroup)

        answerCode= answerGroup.find(class_='TermText')
        print("Answer code: ", answerCode)

        answer = answerGroup.find_all(text=True)
        print("Answer 1: ", answer)

        answer = ' '.join(map(str, answer))
        print("Answer 2: ", answer)

        play(answer)
        print("Final answer: ", answer)
    except:
        # raise
        error += 1
        print("Answer can not be found on quizlet")
                

def google_search(search_term, api_key, cse_id, **kwargs):
    sites = []
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    items = res['items']
    for result in items:
        # for key, value in result.items():
    	#     print("Key: ",key," Value: ", value)
        a = result.get('formattedUrl')
        # print("URL: ",a)
        if a not in sites:
            sites.append(a)
    return sites



def findAnswers(question):
    possibleAnswers = []

    # key = 'import from json'
    # token = 'import from json'
    nums = 5
    result = ""
    for j in google_search(question, key, token, num=nums): 
        getAnswer(j,question)
        # print("Result: ", result1)


def play(data):
    myobj = gTTS(text=str(data), lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("welcome.mp3")


def search(data):
    exam = 'Exam1.csv'
    questions = csv.reader(open(exam, "r"), delimiter=",")

    print("Searching for: ",data)
    for row in questions:
        if data in row[0]:
            print("Found")
            print(row[0+1])
            answer = row[0+1]
            play(answer)
            return True
  

old = []

# need this once to not search
# at the beginning
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
old.append(data)
win32clipboard.CloseClipboard()

while True:
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
    except:
        # remove maybe?
        win32clipboard.EmptyClipboard()
        print("Can't access clipboard")

    if data not in old:
        old.append(data)
        print(data)
        # play(data)
        # search(data)

        found = search(data)
        if found:
            pass
        else:
            # print("Type: ", type(data))
            findAnswers(data)

            if error > 4:
                print("Errors: ", error)
                no = "Not Found"
                print("Not Found")
                play(no)
                error = 0

    else:
        print("Passing")
        time.sleep(3)
        if len(old) > 4:
            old.pop(0)
            print("Popping first in list")


# q = "Active documents are sometimes referred to as"
# findAnswers(q)
