from logging import shutdown
import pyttsx3
import speech_recognition as sr
import datetime

import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit

import smtplib

import sys
import pyautogui
import time

from PyQt5 import QtWidgets, QtCore, QtGui            # pip install PyQt5

from PyQt5.QtCore import QTimer, QTime, QDate, Qt     # pip install PyQt5-tools
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *                         # * for all module in library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from supervUi import Ui_supervUi

# pip install pipwin
# pipwin install pyaudio


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# print(voices[0].id)
engine.setProperty('voices',voices[0].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak(" Good Morning")
    elif hour >12 and hour < 18:
        speak(" Good Afternoon")
    else:
        speak(" Good Evening")
    speak(" I am Super V , how can I help you")


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run (self):
        self.TaskExecution()

    # voice to text
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as s:
            print(" Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(s)
            audio = r.listen(s)

        try:
            print(" Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f" User said : {query}\n")

        except Exception as e:
            speak(" Say that again please ...")
            return "None"
        return query 

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand().lower()
            #logics
            if "open notepad" in self.query:
                path = "C:\\Windows\\notepad.exe"
                os.startfile(path)
            elif "open command prompt" in self.query:
                os.system("start cmd")
            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam',img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif "play music" in self.query:
                music_dir = "C:\\Users\\VISHAL\\Documents\\ALL FILES\\Mobile\\Redmi 9 prime\\Download"

                songs = os.listdir(music_dir)
                """rd = random.choice(songs)
                os.startfile(os.path.join(music_dir,rd))"""
                for song in songs:
                    if song.endswith(".mp3"):
                        os.startfile(os.path.join(music_dir,song))
                        break
            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f" Your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak(" Searching wikipedia....")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences = 2 )
                speak(" According to Wikipedia")
                speak(results)
                print(results)
            elif "open youtube" in self.query:
                webbrowser.open('www.youtube.com')
            elif "open facebook" in self.query:
                webbrowser.open('www.facebook.com')
            elif "open google" in self.query:
                speak(" Sir, what should i search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f'https://www.google.com/search?q={cm}')

            elif "no thanks" in self.query:
                speak("Thank you for using me, Have a nice day")
                sys.exit()

            elif "switch window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "take screenshot"in self.query:
                speak("sir,please tell name for the screenshot file")
                name = self.takecommand().lower()
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("i am done sir, the screenshot is saved in our main")

            speak(" Do you have any other work..")


#defining object of class main

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_supervUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../Downloads/Ui/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("../../Downloads/Ui/Jarvis_Loading_Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
superv = Main()
superv.show()
exit(app.exec_())

# GUI

# In windows cmd 
#pip install pyqt5
#pip install pyqt5-tools


# After Qtdesigner
#open folder path cmd run command
#pyuic5 SuperVUi.ui > SuperVUi.py