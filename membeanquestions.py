import csv
import random
import time
import os
from chromedriverauto import chromedriverautodownload

# Ensures chromedriver is donwloaded
# chromedriverautodownload()

# System call
os.system("")
counter = 0
fullQuizableWordList = []
quizQuestion = []
answerOneList = []
answerTwoList = []
answerThreeList = []
correctAnswerList = []
wordDefinition = []
rank = []
synonym = []
problemWeight = []
wordRecited = []
filename = "quizzablewordstester.csv"


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def weightCalculator(timeElapsed, correct, rank):
    element = int(timeElapsed)
    problem = 0
    if rank == 1:
        problem = 2
    if rank == 0:
        problem = 4
    if rank < 0:
        problem = -8*rank
    if correct:
        return element*50*problem
    else:
        return element*50*10*problem

with open(filename, 'r') as file:
    reader = csv.reader((line.replace('\0', '') for line in file))
    i = 0

    for row in reader:
        if i != 0:
            fullQuizableWordList.append(row[0])
            quizQuestion.append(row[1])
            answerOneList.append(row[2])
            answerTwoList.append(row[3])
            answerThreeList.append(row[4])
            correctAnswerList.append(row[5])
            wordDefinition.append(row[6])
            rank.append(row[7])
            synonym.append(row[8])
            problemWeight.append(int(row[9]))
        i = i + 1

while True:
    quizableListNumber = []
    while len(wordRecited) > 10:
        wordRecited.pop(0)
    with open(filename, 'r+', newline='') as re:  # Here your csv file
        r = csv.reader((line.replace('\0', '') for line in re))
        w = csv.writer(re)
        lines = list(r)
        for p in range(len(wordRecited)):
            weight = int(lines[wordRecited[p] + 1][9]) + (p - 3) * 200
            if weight <= 0:
                weight = 1
            if p > len(wordRecited)-2 and (len(fullQuizableWordList) - rank.count(2)) > 2:
                weight = 0
            lines[wordRecited[p] + 1][9] = weight
        writer = w
        re.truncate(0)
        writer.writerows(lines)
        problemWeight.clear()
        for z in range(len(lines)):
            if z != 0:
                problemWeight.append(int(lines[z][9]))
    for i in range(len(fullQuizableWordList)):
        quizableListNumber.append(int(i))
    randomQuestion = random.choices(quizableListNumber, problemWeight)
    randomQuestion = int(randomQuestion[0])
    if int(rank[int(randomQuestion)]) < 1:
        if randomQuestion in wordRecited:
            wordRecited.remove(randomQuestion)
        wordRecited.append(randomQuestion)
        incorrect = False
        while not incorrect:
            startTime = time.perf_counter()
            print(color.BOLD + "Word: " + color.END + color.BLUE + fullQuizableWordList[randomQuestion] + color.END)
            print(quizQuestion[randomQuestion])
            print("\n" + "A. " + answerOneList[randomQuestion])
            print("B. " + answerTwoList[randomQuestion])
            print("C. " + answerThreeList[randomQuestion] + "\n")
            answer = input("Answer:").lower()
            timeElapsed = time.perf_counter() - startTime
            if answer == correctAnswerList[randomQuestion]:
                print("Correct")
                print(color.BOLD + "Definition: " + color.END + color.BLUE + wordDefinition[randomQuestion] + color.END)
                if synonym[randomQuestion] != "none":
                    synonymsplit = synonym[randomQuestion].split(", ")
                    print(color.BOLD + "Synonyms: " + color.END, end="")
                    for e in range(len(synonymsplit)):
                        if e != 0:
                            print(", " + color.RED + synonymsplit[e] + color.END, end="")
                        else:
                            print(color.RED + synonymsplit[e] + color.END,  end="")
                print("\n")
                incorrect = True
                with open(filename, 'r+', newline='') as re:  # Here your csv file
                    r = csv.reader((line.replace('\0', '') for line in re))
                    w = csv.writer(re)
                    lines = list(r)
                    lines[randomQuestion+1][7] = int(lines[randomQuestion+1][7]) + 1
                    weight = weightCalculator(timeElapsed, True, lines[randomQuestion+1][7])
                    lines[randomQuestion+1][9] = weight
                    writer = w
                    re.truncate(0)
                    writer.writerows(lines)
                    rank.clear()
                    problemWeight.clear()
                    for z in range(len(lines)):
                        if z != 0:
                            rank.append(lines[z][7])
                            problemWeight.append(int(lines[z][9]))
            elif answer.lower() == "progress" or answer.lower() == "p":
                maxnumbers = len(rank) * 2
                numberscompleted = 0
                for i in rank:
                    numberscompleted += int(i)
                print(numberscompleted, "/", maxnumbers)
                print(str(round(numberscompleted/maxnumbers * 100, 3)) + "%")
            elif answer == "a" or answer == "b" or answer == "c":
                print(color.RED + "\n" + "Incorrect. Please try again."+ "\n" + color.END)
                with open(filename, 'r+', newline='') as re:  # Here your csv file
                    r = csv.reader((line.replace('\0', '') for line in re))
                    w = csv.writer(re)
                    lines = list(r)
                    lines[randomQuestion+1][7] = int(lines[randomQuestion+1][7]) - 1
                    weight = weightCalculator(timeElapsed, False, lines[randomQuestion+1][7])
                    lines[randomQuestion+1][9] = weight
                    writer = w
                    re.truncate(0)
                    writer.writerows(lines)
                    rank.clear()
                    problemWeight.clear()
                    for z in range(len(lines)):
                        if z != 0:
                            rank.append(lines[z][7])
                            problemWeight.append(int(lines[z][9]))
            else:
                print(color.RED + "\n" + "Please select a given answer choice."+ "\n" + color.END)
    elif int(rank[int(randomQuestion)]) == 1:
        if randomQuestion in wordRecited:
            wordRecited.remove(randomQuestion)
        wordRecited.append(randomQuestion)
        incorrect = False
        tries = 0
        while not incorrect:
            capitalize = False
            word = fullQuizableWordList[randomQuestion]
            startTime = time.perf_counter()
            print(color.BOLD + "Fill in the Blank: " + color.END)
            wordsplit = wordDefinition[randomQuestion].split(word)
            if len(wordsplit) == 1:
                capitalize = True
                wordsplit = wordDefinition[randomQuestion].split(word.capitalize())
            if len(word) > 15: # change to change up position of shown letters
                type = 0
                blanks = int(len(word)) - 4
                fillin = word[:2]
                fillin1 = word[-0:]
            else:
                type = 1
                blanks = int(len(word)) - 1
                fillin = word[:1]
                fillin1 = ""
            actualBlanks = ""
            for i in range(blanks):
                actualBlanks += "-"
            if capitalize:
                fillin = fillin.capitalize()
            try:
                print(wordsplit[0] + color.BLUE + fillin + actualBlanks + fillin1 + color.END + wordsplit[1])
            except:
                print(wordsplit[0] + "( " + color.BLUE + fillin + actualBlanks + fillin1 + color.END + ")" + color.PURPLE + " [Error adding blanks]" + color.END)
            if tries > 0:
                if synonym[randomQuestion] != "none":
                    synonymsplit = synonym[randomQuestion].split(", ")
                    print(color.BOLD + "Synonyms: " + color.END, end="")
                    for e in range(len(synonymsplit)):
                        if e != 0:
                            print(", " + color.RED + synonymsplit[e] + color.END, end="")
                        else:
                            print(color.RED + synonymsplit[e] + color.END, end="")
                    print("\n", end="")
            if tries >= 2:
                print("Correct Answer is: " + word)
                answer = input("\nRetype word to continue: ")
            else:
                answer = input("\n" + "Answer: ")
            timeElapsed = time.perf_counter() - startTime
            actualAnswer = word[2:-2]
            if type == 1:
                actualAnswer = word[1:-1]
            if (answer.lower() == word or answer.lower() == actualAnswer) and tries >= 2:
                incorrect = True
                print("\n")
            elif answer.lower() == word or answer.lower() == actualAnswer:
                print("Correct")
                if synonym[randomQuestion] != "none":
                    synonymsplit = synonym[randomQuestion].split(", ")
                    print(color.BOLD + "Synonyms: " + color.END, end="")
                    for e in range(len(synonymsplit)):
                        if e != 0:
                            print(", " + color.RED + synonymsplit[e] + color.END, end="")
                        else:
                            print(color.RED + synonymsplit[e] + color.END, end="")
                print("\n")
                incorrect = True
                with open(filename, 'r+', newline='') as re:  # Here your csv file
                    r = csv.reader((line.replace('\0', '') for line in re))
                    w = csv.writer(re)
                    lines = list(r)
                    lines[randomQuestion + 1][7] = int(lines[randomQuestion + 1][7]) + 1
                    weight = weightCalculator(timeElapsed, True, lines[randomQuestion+1][7])
                    lines[randomQuestion+1][9] = weight
                    writer = w
                    re.truncate(0)
                    writer.writerows(lines)
                    rank.clear()
                    problemWeight.clear()
                    for z in range(len(lines)):
                        if z != 0:
                            rank.append(lines[z][7])
                            problemWeight.append(int(lines[z][9]))
            elif answer == "OVERRIDE":
                print("Correct answer is: " + word + "\n")
                confirmation = input("Confirm Override [y]: ")
                incorrect = True
                if confirmation == "" or confirmation == "y":
                    print(color.PURPLE + "OVERRIDED" + "\n" + color.END)
                    with open(filename, 'r+', newline='') as re:  # Here your csv file
                        r = csv.reader((line.replace('\0', '') for line in re))
                        w = csv.writer(re)
                        lines = list(r)
                        lines[randomQuestion + 1][7] = int(lines[randomQuestion + 1][7]) + tries
                        if lines[randomQuestion + 1][7] > 2:
                            lines[randomQuestion + 1][7] == 2
                        writer = w
                        re.truncate(0)
                        writer.writerows(lines)
                        rank.clear()
                        problemWeight.clear()
                        for z in range(len(lines)):
                            if z != 0:
                                rank.append(lines[z][7])
                                problemWeight.append(int(lines[z][9]))
                else:
                    print(color.PURPLE + "CANCELED OVERRIDE" + "\n" + color.END)
            elif answer.lower() == "progress" or answer.lower() == "p":
                maxnumbers = len(rank) * 2
                numberscompleted = 0
                for i in rank:
                    numberscompleted += i
                print(numberscompleted, "/", maxnumbers)
                print(str(numberscompleted/maxnumbers * 100) + "%")
            else:
                print(color.RED + "\n" + "Incorrect. Please try again." + "\n" + color.END)
                with open(filename, 'r+', newline='') as re:  # Here your csv file
                    r = csv.reader((line.replace('\0', '') for line in re))
                    w = csv.writer(re)
                    lines = list(r)
                    lines[randomQuestion + 1][7] = int(lines[randomQuestion + 1][7]) - 1
                    weight = weightCalculator(timeElapsed, False, lines[randomQuestion+1][7])
                    lines[randomQuestion+1][9] = weight
                    writer = w
                    re.truncate(0)
                    writer.writerows(lines)
                    rank.clear()
                    problemWeight.clear()
                    for z in range(len(lines)):
                        if z != 0:
                            rank.append(lines[z][7])
                            problemWeight.append(int(lines[z][9]))
            tries += 1
    else:
        counter += 1
        if counter == 10:

            counter = 0
            done = True
            for i in range(len(fullQuizableWordList)):
                if int(rank[i]) < 2:
                    done = False

            if done == False:

                with open(filename, 'r+', newline='') as re:  # Here your csv file

                    r = csv.reader((line.replace('\0', '') for line in re))
                    w = csv.writer(re)
                    lines = list(r)
                    for i in range(len(fullQuizableWordList)):
                        if int(lines[i+1][7]) == 2:
                            lines[i + 1][9] = 0
                    writer = w
                    re.truncate(0)
                    writer.writerows(lines)
                    rank.clear()
                    problemWeight.clear()
                    for z in range(len(lines)):
                        if z != 0:
                            rank.append(lines[z][7])
                            problemWeight.append(int(lines[z][9]))
            if done == True:
                break
print("Congratulations! You learned all the words")
