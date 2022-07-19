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

google_key = 'f7170e885e46770e0'
error = 0
old = []

def getAnswer(pageUrl,question):
    # print('\n')

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
    'referer':'https://www.google.com/'
    }
    answer = ''

    # needed because some can be searched
    # but don't exist anymore
    try:
        page = requests.get(str(pageUrl),headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find(class_="UIHeading UIHeading--one").text
        print("Page URL: ", pageUrl)
        print("Page title: ",title)
        print("Searching for:", question)
    except:
        # raise  
        print("Can't access site")
        return
    
    try:
        title = soup.find(class_="UIHeading UIHeading--one").text

        # if the question cant be found then it fails here
        questionText =soup.find(string=re.compile(question, flags=re.I))
        termList = soup.find(class_='SetPageTerm')
        # print("Termlist: ", termList)
        answerList = termList.find_all('SetPageTerm-wordText')
        # print("answerList: ", answerList)
        # if the question is on the opposite side
        termWhole = questionText.parent.parent.parent.parent.parent
        # print("term whole: ", termWhole)
        answerGroup = termWhole.find(class_='SetPageTerm-definitionText')
        # print("answer group: ", answerGroup)
        answerCode= answerGroup.find(class_='TermText')
        # print("answer code: ", answerCode)
        answer = answerGroup.find_all(text=True)
        answer = ' '.join(map(str, answer))
        # print("Answer: ",answer,'\n')
    except:
        pass

    #split question
    if len(answer) >= len(question):
        # scenario_2(answer,soup)
        # print("term whole: ", termWhole)
        answerGroup = termWhole.find(class_='SetPageTerm-wordText')
        # print("answer group: ", answerGroup)
        answerCode= answerGroup.find(class_='TermText')
        # print("answer code: ", answerCode)
        answer = answerGroup.find_all(text=True)
        answer = ' '.join(map(str, answer))
        print("Answer: ",answer,'\n')
        play(answer)
        return

    if title == 'Page Unavailable':
        pass
    elif answer == question:
        scenario_2(question, soup)
    elif answer == "":
        scenario_3(question, soup)
    elif answer == "...":
        pass
    elif answer != question and answer != "":
        print("Answer: ",answer,'\n')
        play(answer)
    else:
        print("Answer not found.")

def find_word(text, search):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
        # print("Found word: ", result)
        return 1
   else:
      return 0

def scenario_2(desired_question, soup):
    print("Scenario 2")
    # Find the table with all the questions and answers.
    answer_table = soup.find_all("div", class_="SetPageTerm-content")
    
    # Iterate over the rows and find the question that matches the one passed in the args.
    for row in answer_table:
        answer, question = row.find_all(class_="TermText")
        print("Desired: " ,desired_question.lower(),"\n", "Question: ", question.text.lower())
        if question.text.lower() == desired_question.lower():
            print(f"Answer: {answer.text}\n")
            print("Question:", question)
            play(answer)
            # return

def scenario_3(desired_question, soup):
    print("Scenario 3")
    global error
    # Get a list of the words forming the desired question. It will be used later for getting close matches.
    words = desired_question.split(" ")
    # print("\n")
    # print("Words: ", words )

    # Get a table with all the questions and answers.
    answer_table = soup.find_all("div", class_="SetPageTerm-content")
    
    # These variables will store the index for the best match, and the biggest amount of matches.
    best_match_index = None
    biggest_match = 0
    
    # Iterate over the table
    for i, row in enumerate(answer_table):
        question, answer = row.find_all(class_="TermText")

        # Get close matches for each word forming the question from this row,
        # and add the number of matches into a variable
        current_matches = 0
        # current_matches2 = 0
        for word in question.text.split(" "):
            # print("For word: ", word)
            # current_matches += len(get_close_matches(word, words))
            for term in words:
                a = find_word(word,term)
                current_matches = current_matches + a
            # print

        # print("Current matches: ", current_matches)
        # If necessary, replace the best match with the current match.
        if current_matches > biggest_match:
            biggest_match = current_matches
            best_match_index = i
    if biggest_match < 3:
        error += 1
        return

    question, answer = answer_table[best_match_index].find_all(class_="TermText")
    

    print(len(question.text), " > " , (len(desired_question)+40))
    if len(question.text) > (len(desired_question)+35):
        # print(f"Closest Question: {question.text}")
        # print("Length of Close question: ", len(question.text))
        error += 1
        return
    
    if len(answer.text) > (len(desired_question)+40):
        error += 1
        return
    
    # if desired_question in answer.text:
    #     scenario_2(desired_question, soup)

    print(f"Closest Question: {question.text}")
    print("Length of Actaul question: ", len(desired_question))
    print("Length of Close question: ", len(question.text))
    print("Total match: ", biggest_match)
    print(f"Answer: {answer.text}\n")   

    # play("Closest Question")
    # play(question.text)
    # play("Answer")
    play(answer.text)       

def google_search(search_term, api_key, cse_id, **kwargs):
    sites = []
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=str(search_term), cx=cse_id, **kwargs).execute()
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
    nums = 3
    index = 1
    result = ""
    for j in google_search(question, key, token, num=nums):
        print("Search # ", index)
        index += 1
        getAnswer(j,question)
        print("\n")
        # print("Result: ", result1)

def play(data,language='en'):
    myobj = gTTS(text=str(data), lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("welcome.mp3")

def search(data):
    exam = 'Exam1.csv'
    # exam2 = 'Exam2.csv'
    questions = csv.reader(open(exam, "r"), delimiter=",")
    # questions2 = csv.reader(open(exam2, "r"), delimiter=",")

    print("Searching for: ",data)
    for row in questions:
        if data in row[0]:
            print("Found")
            print(row[0+1])
            answer = row[0+1]
            play(answer)
            return True

def initial_run():
    # need this once to not search
    # at the beginning
    win32clipboard.OpenClipboard()
    data1 = "none"
    data2 = win32clipboard.SetClipboardText(data1, win32clipboard.CF_UNICODETEXT)
    old.append(data2)
    # win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def main():
    global error
    while True:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            # print(data)
            win32clipboard.CloseClipboard()
        except:
            # remove maybe?
            # win32clipboard.CloseClipboard()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            print("Can't access clipboard")
        # print(len(old))
        if data not in old and data != "none":
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


if __name__ == "__main__":
    initial_run()
    main()