from googlesearch import search 
import requests
from bs4 import BeautifulSoup
import re
import os,time
from gtts import gTTS
# from answers import play
from googleapiclient.discovery import build
import json


# https://cloud.google.com/

f = open('token.json')
data = json.load(f)
    
key = data['key'][0]
token = data['token'][0]

nums = 2

term = '_________ is a repository of information linked together from points all over the world.'


def play(data):
    language = 'en'
    myobj = gTTS(text=str(data), lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("welcome.mp3")

def cookies():
    googleTrendsUrl = 'https://google.com'
    response = requests.get(googleTrendsUrl)
    if response.status_code == 200:
        g_cookies = response.cookies.get_dict()
        print(g_cookies)
        return g_cookies
    return ""

def getAnswer(pageUrl,question):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
    'referer':'https://www.google.com/'
    }

    page = requests.get(str(pageUrl),headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find(class_="UIHeading UIHeading--one").text
    print("Page title: ",title)
    print("Searching for: ", question)
    print("Page URL: ", pageUrl)

    time.sleep(5)
    
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
    # term = "\"{}\"".format(question) + " site:quizlet.com"
    #print(query)

    possibleAnswers = []

    # key = 'import from json'
    # token = 'import from json'
    nums = 3
    result = ""
    for j in google_search(question, key, token, num=nums): 
        result1 = getAnswer(j,question)
        print("Result: ", result1)



        
# q = "The _________ is a standard for specifying any kind of information on the Internet."
# findAnswers(q)