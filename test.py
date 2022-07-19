import requests,re
from bs4 import BeautifulSoup

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
    
    try:
        title = soup.find(class_="UIHeading UIHeading--one").text
        questionText =soup.find(string=re.compile(question, flags=re.I))
        termList = soup.find(class_='SetPageTerm')
        answerList = termList.find_all('SetPageTerm-wordText')

        # fails right below here at termWhole
        termWhole = questionText.parent.parent.parent.parent.parent
        answerGroup = termWhole.find(class_='SetPageTerm-definitionText')
        answerCode= answerGroup.find(class_='TermText')
        answer = answerGroup.find_all(text=True)
        answer = ' '.join(map(str, answer))
        print(answer)
    except:
        print("Answer can not be found on quizlet")
        raise


        # except Exception as error:
        #     print(error)


url = 'https://quizlet.com/11473234/test-5-flash-cards/'
question = '_____________ is a language for creating Web pages.'
# URL:  https://quizlet.com/96552344/5-flash-cards/
# URL:  https://quizlet.com/248518257/data-exam-3-flash-cards/
# URL:  https://quizlet.com/110576215/www-dns-ch-26-flash-cards/
# URL:  https://quizlet.com/11473234/test-5-flash-cards/
# URL:  https://quizlet.com/135369198/4-flash-cards/

getAnswer(url,question)
getAnswer(url,question)
