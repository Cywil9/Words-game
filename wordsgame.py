from flask import Flask, render_template, url_for, request, redirect, flash, session

import csv
import random
import time
import datetime
import contains
import os

from threading import Thread

app = Flask(__name__)

@app.route('/')
def display_home():
	return render_template("home.html",
				the_title="Words Game",
				game_url=url_for("playgame"),
				top_url=url_for("top10") )

@app.route('/game')
def playgame():
    #session['sourceWord'] = randWord()
    sourceWord = randWord()    
    session['startTime'] = time.time()
    strTime = time.strftime("%H:%M:%S")
    return render_template("game.html",
                            the_title="Please enter 7 words",
                            the_source = sourceWord,
                            the_startTime = strTime,
                            the_save_url=url_for("saveformdata"))

@app.route('/saveform', methods=["POST"])
def saveformdata():
#finish time
#total time taken
    session['globalList'] = []
    session['finishTime'] = time.time()
    session['totalTime'] = session['finishTime'] - session['startTime']
#    session['totalTime'] = session['totalTime'] % 60
    userInput = request.form.getlist('word')
    sourceWord = request.form["sourceW"]
    results = []
    newList = []
    allOk = True

    for word in userInput:
        results.append(wordCheck(sourceWord, word))
        newList.append(word)
        
    
    for result in results:
        if result != "Good Word":
            allOk = False
        else:
            pass

    if allOk != True:
        return render_template("results.html",
                                the_title="You lose",
                                the_wordResults = zip(userInput, results),
                                home_url=url_for("display_home"),
                                game_url=url_for("playgame"))
    else:
        return render_template("success.html",
                            the_title="You Win",
                            the_time = session['totalTime'],
                            home_url=url_for("display_home"),
                            the_username_url = url_for("username"))

@app.route('/username', methods=["POST"])
def username():
    session['username'] = request.form['user_name']

    if session['username'] == "":
        session['username'] = "Guest"

    topRec = []
    with open(os.path.dirname(os.path.realpath(__file__))+"/top.txt", 'r') as top:
        the_top = top.read().splitlines()

    for row in the_top:
        if not row:
            continue
        temp = row.split()
        topRec.append([float(temp[0]), temp[1]])
    
    topRec.append([(session['totalTime']), session['username']])
    
    topRec = sorted(topRec, key=lambda  x: x[0])

    topRecStr = ""
    for row in topRec:
        topRecStr += "\t".join(map(str, row)) + "\n"

    with open(os.path.dirname(os.path.realpath(__file__))+"/top.txt", 'w') as top:
        print(topRecStr, file=top)


    times =[]
    names =[]
    count =0
    with open(os.path.dirname(os.path.realpath(__file__))+"/top.txt") as f:
        f_reader = csv.reader(f, delimiter="\t")
        for row in f_reader:
            if len(row):
                if session['totalTime'] == float(row[0]):
                    pos = count+1
                if count < 10:
                    times.append(row[0])
                    names.append(row[1])
            count += 1
                

    
            
    return render_template("userplace.html",
                            the_title="Top 10",
                            the_username = session['username'],
                            the_time = session['totalTime'],
                            the_pos = pos,
                            play_msg = "Go on, give it another go!",
                            the_top10 = zip(times, names),
                            home_url=url_for("display_home"),
                            game_url=url_for("playgame"))

@app.route('/top')
def top10():
    times =[]
    names =[]
    count =0
    with open(os.path.dirname(os.path.realpath(__file__))+"/top.txt") as f:
        f_reader = csv.reader(f, delimiter="\t")
        for row in f_reader:
            if len(row):
                times.append(row[0])
                names.append(row[1])
                count += 1
                if count == 10:
                    break

    return render_template("userplace.html",
                            the_title="Top 10",
                            the_top10 = zip(times, names),
                            play_msg = "Give it a go!",
                            home_url=url_for("display_home"),
                            game_url=url_for("playgame"))

def randWord():
    line = ""
    while len(line.strip()) < 8:
        line = random.choice(open(os.path.dirname(os.path.realpath(__file__))+"/words.txt").readlines())
    return line

def wordCheck(sourceWord, word):
    goodWord = ""
    word = word.lower()
    word = word.strip()

    with open(os.path.dirname(os.path.realpath(__file__))+"/words.txt", "r") as myWords:
        allWords = myWords.read().splitlines()

    if word == "":
        errMsg = "No word"
        return errMsg
    if 3 > len(word):
        errMsg = "Word entered is too short (minimum 3 characters)"
        return errMsg
    if word == sourceWord.strip():
        errMsg = "Word entered is the same as the source word"
        return errMsg  
    if word not in allWords:
        errMsg = "Word is not in the dictonary"
        return errMsg
    if not contains.contains(sourceWord, word):
        errMsg = "The letters used in the word are not in the source word"
        return errMsg
    if word in session['globalList']:
        return "Duplicate"
   
    session['globalList'].append(word)     

    return "Good Word"


app.config['SECRET_KEY'] = 'supersecret'
#app.run(debug=True)