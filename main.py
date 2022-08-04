# Written by Alex Bertran
# V0.1 7/17/2022
# V0.2 7/18/2022

import cv2
import numpy as np
import random
import keyboard
import time
from collections import defaultdict

# Creating global numpy arrays for all screens
img = np.zeros((1080,1920,3), dtype=np.uint8)
home = np.zeros((1080,1920,3), dtype=np.uint8)
singleplayer = np.zeros((1080,1920,3), dtype=np.uint8)
statistics = np.zeros((1080,1920,3), dtype=np.uint8)
playing = np.zeros((1080,1920,3), dtype=np.uint8)
robotics = False
normal = False
hard = False

# Defining globals
screenStatus = 1
errors = 0
word = ""
guess = ""
guessList = list()
wordList = list()
ready = False
initialization = True
textCoord = 0
coords = (0, 0)

letters1 = ('q','w','e','r','t','y','u','i','o','p')
letters2 = ('a','s','d','f','g','h','j','k','l')
letters3 = ('z','x','c','v','b','n','m')

keyUsed = list()
guesses = list()
guessedLetters = list()

for i in range(26):
    guesses.append(1)
    keyUsed.append(0)

# Color Dictionary
dictionary = {}
for i in range(26):
    dictionary["{}".format(i)] = (175, 175, 175)

def startup():
    # The startup function serves to create the base images required to play the game
    global home, singleplayer, playing, normal, hard, statistics, screenStatus
    
    # Home Screen
    home = cv2.putText(home, "H A N G M A N", (330, 400), cv2.FONT_HERSHEY_TRIPLEX, 5, (9, 9, 84), 5, cv2.LINE_AA)
    home = cv2.putText(home, "H A N G M A N", (333, 403), cv2.FONT_HERSHEY_TRIPLEX, 5, (180, 205, 255), 5, cv2.LINE_AA)
        # Singleplayer Button
    home = cv2.rectangle(home, (57,537), (900, 810), (47, 47, 118), -1, cv2.LINE_AA)
    home = cv2.rectangle(home, (60,540), (900, 810), (127, 127, 238), -1, cv2.LINE_AA)
    home = cv2.putText(home, "Singleplayer", (190, 710), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
        # Statistics Button
    home = cv2.rectangle(home, (1017, 537), (1860, 810), (118, 47, 47), -1, cv2.LINE_AA)
    home = cv2.rectangle(home, (1020, 540), (1860, 810), (238, 127, 127), -1, cv2.LINE_AA)
    home = cv2.putText(home, "Statistics", (1220, 710), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
        # Close Game Button
    home = cv2.line(home, (1896, 4), (1916, 24), (52, 52, 245), 3, cv2.LINE_AA)
    home = cv2.line(home, (1916, 4), (1896, 24), (52, 52, 245), 3, cv2.LINE_AA)

    # Singleplayer
    singleplayer = cv2.line(singleplayer, (1896, 4), (1916, 24), (52, 52, 245), 3, cv2.LINE_AA)
    singleplayer = cv2.line(singleplayer, (1916, 4), (1896, 24), (52, 52, 245), 3, cv2.LINE_AA)
        # Select Difficulty Text
    singleplayer = cv2.putText(singleplayer, "Select Difficulty", (400, 300), cv2.FONT_HERSHEY_TRIPLEX, 4, (9, 9, 84), 4, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Select Difficulty", (403, 303), cv2.FONT_HERSHEY_TRIPLEX, 4, (180, 205, 255), 4, cv2.LINE_AA)
        # Robotics Themed Button
    singleplayer = cv2.rectangle(singleplayer, (27, 447), (630, 1000), (47, 47, 118), -1, cv2.LINE_AA)
    singleplayer = cv2.rectangle(singleplayer, (30, 450), (630, 1000), (127, 127, 238), -1, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Robotics", (130, 700), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Themed", (145, 800), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
        # Normal Mode Button
    singleplayer = cv2.rectangle(singleplayer, (657, 447), (1260, 1000), (47, 118, 47), -1, cv2.LINE_AA)
    singleplayer = cv2.rectangle(singleplayer, (660, 450), (1260, 1000), (127, 238, 127), -1, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Normal", (790, 700), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Mode", (835, 800), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
        # Hard Mode Button
    singleplayer = cv2.rectangle(singleplayer, (1287, 447), (1890, 1000), (118, 47, 47), -1, cv2.LINE_AA)
    singleplayer = cv2.rectangle(singleplayer, (1290, 450), (1890, 1000), (238, 127, 127), -1, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Hard", (1465, 700), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    singleplayer = cv2.putText(singleplayer, "Mode", (1465, 800), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    
    # Exit on all playing screens
    playing = cv2.line(playing, (1896, 4), (1916, 24), (52, 52, 245), 3, cv2.LINE_AA)
    playing = cv2.line(playing, (1916, 4), (1896, 24), (52, 52, 245), 3, cv2.LINE_AA)
    
    # Statistics
    statistics = cv2.putText(statistics, "Statistics", (640, 120), cv2.FONT_HERSHEY_TRIPLEX, 4, (9, 9, 84), 4, cv2.LINE_AA)
    statistics = cv2.putText(statistics, "Statistics", (643, 123), cv2.FONT_HERSHEY_TRIPLEX, 4, (180, 205, 255), 4, cv2.LINE_AA)
    statistics = cv2.line(statistics, (640, 200), (640, 980), (255, 255, 255), 5, cv2.LINE_AA)
    statistics = cv2.line(statistics, (1280, 200), (1280, 980), (255, 255, 255), 5, cv2.LINE_AA)
    statistics = cv2.putText(statistics, "Robotics", (100, 220), cv2.FONT_HERSHEY_TRIPLEX, 3, (127, 127, 238), 3, cv2.LINE_AA)
    statistics = cv2.putText(statistics, "Normal", (770, 220), cv2.FONT_HERSHEY_TRIPLEX, 3, (127, 238, 127), 3, cv2.LINE_AA)
    statistics = cv2.putText(statistics, "Hard", (1500, 220), cv2.FONT_HERSHEY_TRIPLEX, 3, (238, 127, 127), 3, cv2.LINE_AA)
    
    statistics = cv2.putText(statistics, "Main Menu", (25, 75), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    statistics = cv2.line(statistics, (1896, 4), (1916, 24), (52, 52, 245), 3, cv2.LINE_AA)
    statistics = cv2.line(statistics, (1916, 4), (1896, 24), (52, 52, 245), 3, cv2.LINE_AA)

def detect_click(event,x,y,flags,param):
    global img, screenStatus, errors, letters1, letters2, letters3, guessedLetters, guess, guessList, wordList, word, ready, guesses, keyUsed, robotics, normal, hard, home
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        # Detect close app
        if 1890 <= x <= 1920 and 0 <= y <= 30:
            quit()
        
        # Detect Keyboard Presses
        row1Y = 115
        row2Y = 212
        row3Y = 309
        increment1, increment2, increment3 = 0, 0, 0
             
        if screenStatus == 5 or screenStatus == 7 or screenStatus == 9:
            # Row 1
            for i in range(10):
                row1X = 873 + (97 * increment1)
                if row1X <= x <= (row1X + 93) and row1Y <= y <= (row1Y + 93):
                    if keyUsed[i] == 0:
                        guessedLetters.append(letters1[i])
                        keyUsed.pop(i)
                        keyUsed.insert(i, 1)
                increment1 = increment1 + 1
            # Row 2
            for i in range(9):
                row2X = 903 + (97 * increment2)
                if row2X <= x <= (row2X + 93) and row2Y <= y <= (row2Y + 93):
                    if keyUsed[i + 10] == 0:
                        guessedLetters.append(letters2[i])
                        keyUsed.pop(i + 10)
                        keyUsed.insert(i + 10, 1)
                increment2 = increment2 + 1
            for i in range(7):
                row3X = 973 + (97 * increment3)
                if row3X <= x <= (row3X + 93) and row3Y <= y <= (row3Y + 93):
                    if keyUsed[i + 19] == 0:
                        guessedLetters.append(letters3[i])
                        keyUsed.pop(i + 19)
                        keyUsed.insert(i + 19, 1)
                increment3 = increment3 + 1
            
        # Detect clicks in home screen
        if screenStatus == 1:
            # Detect Singleplayer
            if 60 <= x <= 900 and 540 <= y <= 810:
                screenStatus = 2
            # Detect Statistics
            if 1020 <= x <= 1860 and 540 <= y <= 810:
                screenStatus = 20
        
        # Detect clicks in singleplayer screen
        if screenStatus == 3:
            # Detect Robotics
            if 30 <= x <= 630 and 450 <= y <= 1000:
                screenStatus = 4
            # Detect Normal
            if 660 <= x <= 1260 and 450 <= y <= 1000:
                screenStatus = 6
            # Detect Hard
            if 1290 <= x <= 1890 and 450 <= y <= 1000:
                screenStatus = 8
        
        if screenStatus == 50 or screenStatus == 51:
            if (1290 <= x <= 1890 and 925 <= y <= 1050) or (30 <= x <= 630 and 925 <= y <= 1050):
                img = cv2.rectangle(img, (0,0), (1920, 1080), (0,0,0), -1)
                word = ""
                errors = 0
                ready = False
                initialization = True
                guessList = list()
                guessedLetters = list()
                guesses = list()
                keyUsed = list()
                for i in range(26):
                    guesses.append(1)
                    keyUsed.append(0)
                if 1290 <= x <= 1890 and 925 <= y <= 1050:
                    if robotics:
                        screenStatus = 4
                    elif normal:
                        screenStatus = 6
                    elif hard:
                        screenStatus = 8
                elif 30 <= x <= 630 and 925 <= y <= 1050:
                    screenStatus = 1
                    img = home
        
        if screenStatus == 20:
            if 0 <= x <= 450 and 0 <= y <= 100:
                screenStatus = 1
                img = home

def selectWord(selection):
    global word, wordList, textCoord
    if selection == 4:
        r = random.randrange(1, 12)
        file = 'textFiles/robotics.txt'
    if selection == 6:
        r = random.randrange(1, 503)
        file = 'textFiles/normal.txt'
    if selection == 8:
        r = random.randrange(1, 214)
        file = 'textFiles/hard.txt'
    contents = open(file, 'r')
    words = []
    for line in contents:
        word = contents.readline().lower()
        words.append(line[:-1])
        words.append(word[:-1])
    word = words[r-1]
    wordList = list(word)

def textLength(word):
    global coords
    
    done = False
        
    textImg = np.zeros((540,1920,3), dtype=np.uint8)
    textImg = cv2.putText(textImg, "\"{}\"".format(word), (25, 270), cv2.FONT_HERSHEY_DUPLEX, 5, (255, 255, 255), 5, cv2.LINE_AA)
    
    for x in range(480):
        for y in range(270):
            if textImg[y + 100][1919 - (x * 4)][0] == 255:
                coords = (int(960 - ((1895 - (int(x) * 4)) / 2)), 800)
                done = True
        if done:
            break

def drawStickman():
    global img, lost, errors, screenStatus, robotics, normal, hard
    if errors == 0:
        # Close Game Button
        img = cv2.line(img, (1896, 4), (1916, 24), (52, 52, 245), 3, cv2.LINE_AA)
        img = cv2.line(img, (1916, 4), (1896, 24), (52, 52, 245), 3, cv2.LINE_AA)
        
        # Incorrect Guesses Box
        img = cv2.putText(img, "Guesses", (1147, 97), cv2.FONT_HERSHEY_TRIPLEX, 3, (9, 9, 84), 3, cv2.LINE_AA)
        img = cv2.putText(img, "Guesses", (1150, 100), cv2.FONT_HERSHEY_TRIPLEX, 3, (180, 205, 255), 3, cv2.LINE_AA)
        img = cv2.rectangle(img, (873, 115), (1851, 402), (255, 255, 255), -1, cv2.LINE_AA)
        img = cv2.rectangle(img, (873, 115), (1851, 402), (255, 255, 255), 3, cv2.LINE_AA)
        
        # Drawing Hanging Post (or whatever it's called)
        img = cv2.line(img, (200, 50), (550, 50), (255, 255, 255), 10, cv2.LINE_AA)
        img = cv2.line(img, (200, 50), (200, 500), (255, 255, 255), 10, cv2.LINE_AA)
        img = cv2.line(img, (50, 500), (350, 500), (255, 255, 255), 10, cv2.LINE_AA)
        img = cv2.line(img, (200, 150), (300, 50), (255, 255, 255), 10, cv2.LINE_AA)
        img = cv2.line(img, (550, 50), (550, 175), (255, 255, 255), 10, cv2.LINE_AA)
    
    # Draw parts of man as more errors are made
    if errors == 1:
        img = cv2.circle(img, (550, 200), 25, (0, 0, 255), 10, cv2.LINE_AA)
    if errors == 2:
        img = cv2.line(img, (550, 225), (550, 325), (0, 0, 255), 10, cv2.LINE_AA)
    if errors == 3:
        img = cv2.line(img, (550, 255), (580, 285), (0, 0, 255), 10, cv2.LINE_AA)
    if errors == 4:
        img = cv2.line(img, (550, 255), (520, 285), (0, 0, 255), 10, cv2.LINE_AA)
    if errors == 5:
        img = cv2.line(img, (550, 325), (580, 380), (0, 0, 255), 10, cv2.LINE_AA)
    if errors == 6:
        img = cv2.line(img, (550, 325), (520, 380), (0, 0, 255), 10, cv2.LINE_AA)
        if screenStatus == 5:
            robotics = True
        if screenStatus == 7:
            normal = True
        if screenStatus == 9:
            hard = True
        screenStatus = 50

def drawKeyboard():
    global img, guesses, dictionary
    
    if initialization:
        for i in range(26):
            dictionary[i] = (175, 175, 175)
        intitialization = False
    
    for j in range(26):
        if guesses[j] == 2:
            dictionary[j] = (0, 0, 255)
        if guesses[j] == 3:
            dictionary[j] = (0, 255, 0)
    
    # Row 1
    img = cv2.rectangle(img, (873, 115), (966, 208), dictionary[16], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (970, 115), (1063, 208), dictionary[22], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1067, 115), (1160, 208), dictionary[4], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1164, 115), (1257, 208), dictionary[17], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1261, 115), (1354, 208), dictionary[19], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1358, 115), (1451, 208), dictionary[24], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1455, 115), (1549, 208), dictionary[20], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1553, 115), (1647, 208), dictionary[8], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1651, 115), (1749, 208), dictionary[14], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1753, 115), (1851, 208), dictionary[15], -1, cv2.LINE_AA)
    
    # Row 2
    img = cv2.rectangle(img, (903, 212), (996, 305), dictionary[0], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1000, 212), (1093, 305), dictionary[18], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1097, 212), (1190, 305), dictionary[3], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1194, 212), (1287, 305), dictionary[5], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1291, 212), (1384, 305), dictionary[6], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1388, 212), (1481, 305), dictionary[7], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1485, 212), (1578, 305), dictionary[9], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1582, 212), (1675, 305), dictionary[10], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1679, 212), (1772, 305), dictionary[11], -1, cv2.LINE_AA)
    
    # Row 3
    img = cv2.rectangle(img, (973, 309), (1066, 402), dictionary[25], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1070, 309), (1163, 402), dictionary[23], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1167, 309), (1260, 402), dictionary[2], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1264, 309), (1357, 402), dictionary[21], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1361, 309), (1454, 402), dictionary[1], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1458, 309), (1551, 402), dictionary[13], -1, cv2.LINE_AA)
    img = cv2.rectangle(img, (1555, 309), (1648, 402), dictionary[12], -1, cv2.LINE_AA)
    
    # Place letters on keys
    img = cv2.putText(img, 'Q', (885, 192), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'W', (978, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'E', (1085, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'R', (1181, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'T', (1282, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'Y', (1377, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'U', (1470, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'I', (1585, 192), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'O', (1667, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'P', (1773, 194), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'A', (920, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'S', (1017, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'D', (1114, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'F', (1211, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'G', (1306, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'H', (1402, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'J', (1506, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'K', (1599, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'L', (1696, 291), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'Z', (990, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'X', (1087, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'C', (1182, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'V', (1281, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'B', (1378, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'N', (1473, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    img = cv2.putText(img, 'M', (1566, 388), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)

def Guessing():
    global img, screenStatus, word, coords, guess, guessedLetters, guessList, wordList, ready, dictionary, guesses, errors, keyUsed, robotics, normal, hard
    displayGuess = ""
    errors = 0
    
    # Prepare visuals and logic based on length of word
    length = len(word)
    
    if not ready:
        for i in range(length):
            guess = guess + "_"
            guessList.append("_")
        ready = True
    
    for j in range(length):
        displayGuess = displayGuess + guessList[j] + " "
    
    # Determine correct guess or not
    if len(guessedLetters) >= 1:
        for k in guessedLetters:
            correct = False
            for l in range(len(wordList)):
                if k == wordList[l]:
                    guessList.pop(l)
                    guessList.insert(l, wordList[l])
                    guesses.pop(ord(wordList[l]) - 97)
                    guesses.insert(ord(wordList[l]) - 97, 3)
                    correct = True
            if not correct:
                guesses.pop(ord(k) - 97)
                guesses.insert(ord(k) - 97, 2)
                errors = errors + 1
    
    count = 0
    for i in range(length):
        if guessList[i] == wordList[i]:
            count = count + 1
    if count == length:
        if screenStatus == 5:
            robotics = True
            writeStatistics(0)
            if len(guessedLetters) != 0:
                for i in range(len(guessedLetters) - errors):
                    writeStatistics(2)
                for i in range(len(guessedLetters)):
                    writeStatistics(3)
        if screenStatus == 7:
            normal = True
            writeStatistics(4)
            if len(guessedLetters) != 0:
                for i in range(len(guessedLetters) - errors):
                    writeStatistics(6)
                for i in range(len(guessedLetters)):
                    writeStatistics(7)
        if screenStatus == 9:
            hard = True
            writeStatistics(8)
            if len(guessedLetters) != 0:
                for i in range(len(guessedLetters) - errors):
                    writeStatistics(10)
                for i in range(len(guessedLetters)):
                    writeStatistics(11)
        screenStatus = 51
        
    textLength(displayGuess)
        
    # Clean up guessing page
    img = cv2.rectangle(img, (100, 600), (1900, 1000), (0, 0, 0), -1)
    img = cv2.putText(img, displayGuess, (coords[0] + 135, coords[1]), cv2.FONT_HERSHEY_DUPLEX, 5, (255, 255, 255), 5, cv2.LINE_AA)

def winLoseScreen():
    global img, word, screenStatus, coords

    textLength(word)
    
    img = cv2.rectangle(img, (0, 510), (1900, 1080), (0, 0, 0), -1)
    
    if screenStatus == 50:
        img = cv2.putText(img, "GAME OVER", (370, 660), cv2.FONT_HERSHEY_TRIPLEX, 6, (0, 0, 255), 7, cv2.LINE_AA)
        img = cv2.putText(img, "\"{}\"".format(word), coords, cv2.FONT_HERSHEY_DUPLEX, 5, (0, 100, 255), 5, cv2.LINE_AA)
    
    if screenStatus == 51:
        img = cv2.putText(img, "CORRECT", (520, 660), cv2.FONT_HERSHEY_TRIPLEX, 6, (0, 255, 0), 7, cv2.LINE_AA)
        img = cv2.putText(img, "\"{}\"".format(word), coords, cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 100), 5, cv2.LINE_AA)
        
    # Play again button
    img = cv2.rectangle(img, (1290, 925), (1890, 1050), (175, 175, 175), -1, cv2.LINE_AA)
    img = cv2.putText(img, "Play Again", (1315, 1015), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
    
    # Main menu button
    img = cv2.rectangle(img, (30, 925), (630, 1050), (175, 175, 175), -1, cv2.LINE_AA)
    img = cv2.putText(img, "Main Menu", (55, 1015), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)

def Statistics():
    global img
    
    statsTxt = open(r"textFiles/statistics.txt", "r")
    statsList = []
    for line in statsTxt:
        listPiece = statsTxt.readline()
        statsList.append(line[:-1])
        statsList.append(listPiece[:-1])
    
    img = cv2.rectangle(img, (0,280), (630, 1080), (0,0,0), -1)
    img = cv2.rectangle(img, (650,280), (1270, 1080), (0,0,0), -1)
    img = cv2.rectangle(img, (1290,280), (1920, 1080), (0,0,0), -1)
    
    img = cv2.putText(img, statsList[0], (75, 320), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[1], (75, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[2], (75, 620), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[3], (75, 770), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[4], (745, 320), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[5], (745, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[6], (745, 620), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[7], (745, 770), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[8], (1385, 320), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[9], (1385, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[10], (1385, 620), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    img = cv2.putText(img, statsList[11], (1385, 770), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)  
    
def writeStatistics(statType):
    global screenStatus
    
    statsTxt = open(r"textFiles/statistics.txt", "r")
    statsList = []
    for line in statsTxt:
        listPiece = statsTxt.readline()
        statsList.append(line[:-1])
        statsList.append(listPiece[:-1])

    # Assigning lines to variables (if it doesnt work try removing last 2 parts of string like -.2: or whatever)
    if statsList[12]:
        rGP = int(statsList[12])
    else:
        rGP = 0
    if statsList[13]:
        rGW = int(statsList[13])
    else:
        rGW = 0
    if statsList[14]:
        rCLG1 = int(statsList[14])
    else:
        rCLG1 = 0
    if statsList[15]:
        rCLG2 = int(statsList[15])
    else:
        rCLG2 = 0
    if statsList[16]:
        nGP = int(statsList[16])
    else:
        nGP = 0
    if statsList[17]:
        nGW = int(statsList[17])
    else:
        nGW = 0
    if statsList[18]:
        nCLG1 = int(statsList[18])
    else:
        nCLG1 = 0
    if statsList[19]:
        nCLG2 = int(statsList[19])
    else:
        nCLG2 = 0
    if statsList[20]:
        hGP = int(statsList[20])
    else:
        hGP = 0
    if statsList[21]:
        hGW = int(statsList[21])
    else:
        hGW = 0
    if statsList[22]:
        hCLG1 = int(statsList[22])
    else:
        hCLG1 = 0
    if statsList[23]:
        hCLG2 = int(statsList[23])
    else:
        hCLG2 = 0
    
    statsTxt.close()
    
    statsTxt = open(r"textFiles/statistics.txt", "w")
    statsTxt.write("")
    statsTxt.close()
    statsTxt = open(r"textFiles/statistics.txt", "a")
    
    # Possible message types
    if statType == 0:
        rGW = rGW + 1
    if statType == 1:
        rGP = rGP + 1
    if statType == 2:
        rCLG1 = rCLG1 + 1
    if statType == 3:
        rCLG2 = rCLG2 + 1
        
    if statType == 4:
        nGW = nGW + 1
    if statType == 5:
        nGP = nGP + 1
    if statType == 6:
        nCLG1 = nCLG1 + 1
    if statType == 7:
        nCLG2 = nCLG2 + 1
        
    if statType == 8:
        hGW = hGW + 1
    if statType == 9:
        hGP = hGP + 1
    if statType == 10:
        hCLG1 = hCLG1 + 1
    if statType == 11:
        hCLG2 = hCLG2 + 1
    
    statsTxt.write("Games Played: {}\n".format(rGP))
    statsTxt.write("Games Won: {}\n".format(rGW))
    if rGP != 0:
        statsTxt.write("Win Rate: {:.2f}%\n".format((rGW / rGP) * 100))
    else:
        statsTxt.write("Win Rate: 0%\n")
    if rCLG2 != 0:
        statsTxt.write("Correct Letter Guesses: {:.2f}%\n".format((rCLG1 / rCLG2) * 100))
    else:
        statsTxt.write("Correct Letter Guesses: 0%\n")
    statsTxt.write("Games Played: {}\n".format(nGP))
    statsTxt.write("Games Won: {}\n".format(nGW))
    if nGP != 0:
        statsTxt.write("Win Rate: {:.2f}%\n".format((nGW / nGP) * 100))
    else:
        statsTxt.write("Win Rate: 0%\n")
    if nCLG2 != 0:
        statsTxt.write("Correct Letter Guesses: {:.2f}%\n".format((nCLG1 / nCLG2) * 100))
    else:
        statsTxt.write("Correct Letter Guesses: 0%\n")
    statsTxt.write("Games Played: {}\n".format(hGP))
    statsTxt.write("Games Won: {}\n".format(hGW))
    if hGP != 0:
        statsTxt.write("Win Rate: {:.2f}%\n".format((hGW / hGP) * 100))
    else:
        statsTxt.write("Win Rate: 0%\n")
    if hCLG2 != 0:
        statsTxt.write("Correct Letter Guesses: {:.2f}%\n".format((hCLG1 / hCLG2) * 100))
    else:
        statsTxt.write("Correct Letter Guesses: 0%\n")
    statsTxt.write("{}\n".format(rGP))
    statsTxt.write("{}\n".format(rGW))
    statsTxt.write("{}\n".format(rCLG1))
    statsTxt.write("{}\n".format(rCLG2))
    statsTxt.write("{}\n".format(nGP))
    statsTxt.write("{}\n".format(nGW))
    statsTxt.write("{}\n".format(nCLG1))
    statsTxt.write("{}\n".format(nCLG2))
    statsTxt.write("{}\n".format(hGP))
    statsTxt.write("{}\n".format(hGW))
    statsTxt.write("{}\n".format(hCLG1))
    statsTxt.write("{} ".format(hCLG2))
    
    statsTxt.close()

def main():
    global img, home, screenStatus, errors, playing, statistics
    
    # Run startup function and launch game
    startup()
    img = home
    cv2.namedWindow("hangman", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("hangman", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    cv2.setMouseCallback("hangman", detect_click)
    while True:
        # Display Game (Default = home)
        cv2.imshow("hangman", img)
        cv2.waitKey(1)
        
        # if singleplayer clicked
        if screenStatus == 2:
            img = singleplayer
            screenStatus = 3
        
        # if robotics theme clicked
        if screenStatus == 4:
            selectWord(screenStatus)
            img = playing
            writeStatistics(1)
            screenStatus = 5
        
        # read when on robotics screen
        if screenStatus == 5:
            drawStickman()
            drawKeyboard()
            Guessing()
        
        # if normal mode clicked
        if screenStatus == 6:
            selectWord(screenStatus)
            img = playing
            writeStatistics(5)
            screenStatus = 7
        
        # read when on normal screen
        if screenStatus == 7:
            drawStickman()
            drawKeyboard()
            Guessing()
            
        # if hard mode clicked
        if screenStatus == 8:
            selectWord(screenStatus)
            img = playing
            writeStatistics(9)
            screenStatus = 9
            
        # read when on hard screen
        if screenStatus == 9:
            drawStickman()
            drawKeyboard()
            Guessing()
        
        # if lost
        if screenStatus == 50:
            winLoseScreen()
        
        # if won
        if screenStatus == 51:
            winLoseScreen()
            
        # if stats clicked
        if screenStatus == 20:
            img = statistics
            Statistics()

main()