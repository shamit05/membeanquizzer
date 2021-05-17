import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from datetime import timedelta
from chromedriverauto import chromedriverautodownload
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import pandas as pd

#fullcsvlistvariables
#saving done at end
fullQuizableWordList = []
answerOneList = []
answerTwoList = []
answerThreeList = []
correctAnswerList = []
wordDefinition = []
quizQuestion = []
synonyms = []
#initial chrome setup and username password inputs
chromedriverautodownload()
chromedriver = "chromedriver.exe"
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(chromedriver, options=options)

username = "shamit.surana@franklinsabers.org" #input("Username: ")
password = "Sabers2083" #input("Password (Only for authentication for membean): ")

filename = "quizzablewordstester.csv"
header = ("Word", "Quiz Question", "Answer A", "Answer B", "Answer C", "Correct Answer", "Definition", "Rank", "Synonyms", "Weights")

reset = input("Do you want to reset list completely? (Only reset if errors are thrown) (y/[n]): ")

try:
    with open(filename, 'x') as file: #checks if file exists, if not it creates one
        print("Creating File")
except:
    print("File Exists")
if reset == "y":
    f = open(filename, 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    print("RESET COMPLETE")

#login functionality
driver.get('https://membean.com/login')
print("If Membean doesn't load in 5 seconds due to cloudfare protection open up another tab and go to membean.com/login and wait for it to load")
usernameBox = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'user_username')))
passBox = driver.find_element_by_id("user_password")
signInBox = driver.find_element_by_xpath("//*[@id='login']/div[5]/button")
usernameBox.send_keys(username)
passBox.send_keys(password)
signInBox.click()
time.sleep(3)

#launches quizzable word page
driver.get('https://membean.com/dashboard/all-words')
try:
    quizzableTab =  WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "react-tabs-8")))
except:
    print("Error logging in.")
quizzableTab.click()
wordlist = driver.find_elements_by_class_name("dfn-tooltip-trigger")

#retrieves word list (that are quizable and sets variable)
for element in driver.find_elements_by_class_name("dfn-tooltip-trigger"):
    element_contents = element.get_attribute('innerHTML')
    fullQuizableWordList.append(element_contents)



wordListFilled = []
with open(filename, 'r') as file:
    reader = csv.reader((line.replace('\0', '') for line in file))
    i = 0

    for row in reader:
        if i != 0:
            wordListFilled.append(row[0])
        i = i + 1

with open(filename, "a", newline='') as csvfile:
    initialWriter = csv.writer(csvfile)
    if reset == "y":
        initialWriter.writerow(header)

    actualWordList = 0
    actualWrite = 0

    actualRemove = 0
    actualRemoveList = 0
    for i in range(len(fullQuizableWordList)):
        if fullQuizableWordList[i] not in wordListFilled:
            actualWordList += 1

    for i in range(len(wordListFilled)):
        if wordListFilled[i] not in fullQuizableWordList:
            actualRemoveList += 1

    removelist = []
    for i in range(len(wordListFilled)):
        if wordListFilled[i] not in fullQuizableWordList:
            actualRemove += 1
            removelist.append(i+1)
            print("Removing " +  wordListFilled[i] + " ("+ str(actualRemove) + "/" + str(actualRemoveList) + ")")

    df = pd.read_csv(filename, skiprows=removelist)
    # And output
    df.to_csv(filename, index=False)

for i in range(len(fullQuizableWordList)):
    if fullQuizableWordList[i] not in wordListFilled:
        with open(filename, "a", newline='') as csvfile:
            initialWriter = csv.writer(csvfile)
            actualWrite += 1
            #retrieves specific word
            word = fullQuizableWordList[i]
            url = "https://membean.com/mywords/" + word
            driver.get(url)

            #retrieves question and correct answers
            answers = []
            answerOne = ""
            answerTwoCorrect = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[class='choice answer ']"))).get_attribute('innerHTML')
            answerThree = ""
            for element in driver.find_elements_by_class_name("choice"):
                element_contents = element.get_attribute('innerHTML')
                answers.append(element_contents)
            if answerTwoCorrect == answers[0]:
                answerOne = answers[1]
                answerThree = answers[2]
            elif answerTwoCorrect == answers[1]:
                answerOne = answers[0]
                answerThree = answers[2]
            elif answerTwoCorrect == answers[2]:
                answerOne = answers[0]
                answerThree = answers[1]


            definition = driver.find_element_by_class_name("def-text").get_attribute('innerHTML')
            question = driver.find_element_by_xpath("//*[@id='context']/div/h3").get_attribute('innerHTML')


            # cleans up left over text in question answers
            answerOneCleanUpOne = answerOne.replace("\n<span class=\"result\"></span>\n", '')
            answerOneCleanUpFinal = answerOneCleanUpOne.replace("\n", '')
            answerTwoCorrectCleanUpOne = answerTwoCorrect.replace("\n<span class=\"result\"></span>\n", '')
            answerTwoCorrectCleanUpFinal = answerTwoCorrectCleanUpOne.replace(".\n", '')
            answerThreeCleanUpOne = answerThree.replace("\n<span class=\"result\"></span>\n", '')
            answerThreeCleanUpFinal = answerThreeCleanUpOne.replace("\n", '')
            definitionReplacer = "\n<a class=\"sound\" href=\"#\" id=\"definition-sound\" path=\"audio/wordmeanings/amy-" + word + "\"></a>\n"
            definitionCleanUpOne = definition.replace(definitionReplacer, '')
            definitionCleanUpTwo = definitionCleanUpOne.replace("\n", '')
            definitionCleanUpThree = definitionCleanUpTwo.replace("<em>", '')
            definitionCleanUpFinal = definitionCleanUpThree.replace("</em>", '')
            questionCleanUpOne = question.replace("<strong>Q<span>uiz:</span></strong>\n<span class=\"status wrong hidden\">Try again!</span>\n", '')
            questionCleanUpTwo = questionCleanUpOne.replace("\n", '')
            questionCleanUpThree = questionCleanUpTwo.replace("<em>", '')
            questionCleanUpFinal = questionCleanUpThree.replace("</em>", '')

            # print(answerOne)
            # print(answerOneCleanUpFinal)
            # print(answerTwoCorrect)
            # print(answerTwoCorrectCleanUpFinal)
            # print(answerThree)
            # print(answerThreeCleanUpFinal)

            #randomizes right answer
            randomNumber = random.randint(0, 2)
            if randomNumber == 0:
                answerOneList.append(answerTwoCorrectCleanUpFinal)
                answerTwoList.append(answerOneCleanUpFinal)
                answerThreeList.append(answerThreeCleanUpFinal)
                correctAnswerList.append("a")
            elif randomNumber == 1:
                answerOneList.append(answerOneCleanUpFinal)
                answerTwoList.append(answerTwoCorrectCleanUpFinal)
                answerThreeList.append(answerThreeCleanUpFinal)
                correctAnswerList.append("b")
            elif randomNumber == 2:
                answerOneList.append(answerOneCleanUpFinal)
                answerTwoList.append(answerThreeCleanUpFinal)
                answerThreeList.append(answerTwoCorrectCleanUpFinal)
                correctAnswerList.append("c")
            wordDefinition.append(definitionCleanUpFinal)
            quizQuestion.append(questionCleanUpFinal)

            url = "https://www.thesaurus.com/browse/" + word
            driver.get(url)
            synonym = ""
            temp = 0
            try:
                for element in WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.CLASS_NAME, "css-1kg1yv8") or driver.find_elements(By.CLASS_NAME, "css-1gyuw4i") or driver.find_elements(By.CLASS_NAME, "css-1n6g4vv")):
                    if temp < 3:
                        element_contents = element.get_attribute('innerHTML')
                        synonym += ", " + element_contents
                    temp += 1
            except:
                synonym = "none"
            synonym = synonym.strip(", ")
            synonym = synonym.replace("<!-- --> ","")
            synonym = synonym.replace("<!-- -->", "")
            synonyms.append(synonym)

            # print(fullQuizableWordList)
            # print(answerOneList)
            # print(answerTwoList)
            # print(answerThreeList)
            # print(correctAnswerList)
            # print(wordDefinition)
            # print(quizQuestion)
            z = actualWrite - 1
            initialWriter.writerow([fullQuizableWordList[i], quizQuestion[z], answerOneList[z], answerTwoList[z], answerThreeList[z], correctAnswerList[z], wordDefinition[z], 0, synonyms[z], 300])
            print("Writing " + fullQuizableWordList[i] + " (" + str(actualWrite) + "/" + str(actualWordList) + ")")
