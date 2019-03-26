from gtts import gTTS
import speech_recognition as sr
import webbrowser
import time
from mutagen.mp3 import MP3
import re
import os
import urllib.request
import urllib.parse
from cv2 import VideoCapture
from cv2 import namedWindow
from cv2 import imshow
from cv2 import imwrite
from cv2 import waitKey
from cv2 import destroyWindow
import json
import wikipedia
#database for questions

with open("Q&A.json","r") as f:
    data = json.load(f)

#recognizez your mic
r = sr.Recognizer()
mic = sr.Microphone()

#text-to-speech
def t2s (audio):
    tts=gTTS(text=audio, lang="en")
    tts.save("tts.mp3")
    os.system("tts.mp3")




#main
def main ():
    with mic as source:     # accepts audio though mic

        global command      #globally declares command
        print ("...")
        r.adjust_for_ambient_noise(source)
        audio=r.listen (source)
    try:
        command=r.recognize_google(audio).lower()
        print (command)

    except sr.UnknownValueError: # if program can't hear you says i can't hear you and starts over
        time.sleep(0.5)
        print("I can't hear you!")
        main ()
    return command

def commands():
    if command == "exit":
        exit(0)
    if command == "tell me weather":
        url = "https://www.accuweather.com"
        webbrowser.open_new(url)
        exit(0)
        
# play music in youtube whenever you tell it play something
def music():
    if "play" in command:
        yt_com = re.findall(r'[\w\']+', command) # gets everything in command
        stri = ' '.join(str(e) for e in yt_com[1:]) #joins everything together
        query_string = urllib.parse.urlencode({"search_query" : stri})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        url_music = "http://www.youtube.com/watch?v=" + search_results[0]
        webbrowser.open_new(url_music)
        exit(0)
# when you tell it camera, take a picture or picture it opens up a camera and takes a picture
def camera():
    if command == "camera" or command == "take a picture" or command == "picture":
        t2s("smile")
        tts_time = MP3("tts.mp3")
        time.sleep(tts_time.info.length + 0.5)
        cam = VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    # frame captured without any errors
            namedWindow("Picture")
            imshow("Picture",img)
            waitKey(0)
            destroyWindow("Picture")
            imwrite("pic.jpg",img) #save image
        exit(0)

#assistant
def webpageopen():
    if "open" in command:
        spl_com = re.findall(r'[\w\']+', command)
        url = "https://" + spl_com[1]+ "." + spl_com[2]
        webbrowser.open_new(url)
        exit(0)

#google
def google():
    if "google" in command:
        spl_com = re.findall(r'[\w\']+', command)
        url = "https://www.google.com/search?client=firefox-b-ab&q="
        str1 = '+'.join(str(g) for g in spl_com[1:])
        webbrowser.open_new(url+str1)
        exit(0)

#searching through the database(dictionary)
def search():
    with open("Q&A.json", "r") as f:
        data = json.load(f)
    #if your voice input == to cyber or cyber security or security it will say "what is cyber security about?" key
    if command == "cyber" or command == "cyber security" or command == "security":
        tts = gTTS(text=data["what is cyber security about?"], lang='en')
        mp3bef = MP3("answer.mp3")
        tts.save("answer.mp3")
        os.system("answer.mp3")
        mp3aft = MP3("answer.mp3")

        exit(0)
        #if mp3 file before the new save and after are the same play the same file
        if mp3bef == mp3aft:
            tts.save("answer.mp3")
            os.system("answer.mp3")
            exit(0)

    webpageopen()
    camera()
    music()
    google()
    commands()
    # goes through every key in dictionary questions
    for key in data.keys():
        # goes through every key of the key in dictionary questions
        for k in key:
            if command in k or command == "what" or command == "who":   # if command is in k or command is what or who says more details needed
                tts = gTTS(text="more details needed", lang='en')
                mp3bef = MP3("answer.mp3")
                tts.save("answer.mp3")
                os.system("answer.mp3")
                mp3aft = MP3("answer.mp3")
                exit(0)
                if mp3bef == mp3aft:
                    tts.save("answer.mp3")
                    os.system("answer.mp3")
                    exit(0)

        # if input is in the key of questions if says the value
        if command in key:
            tts = gTTS(text=data[key], lang='en')
            mp3bef = MP3("answer.mp3")
            tts.save("answer.mp3")
            os.system("answer.mp3")
            mp3aft = MP3("answer.mp3")
            exit(0)

            # if mp3 before the save and after the save are the same saves the file all over again and plays
            if mp3bef == mp3aft:
                tts.save("answer.mp3")
                os.system("answer.mp3")
                exit(0)

    if command not in key:
        result = wikipedia.summary(command)
        add = {command: result}

        with open('Q&A.json') as f:
            data = json.load(f)

        data.update(add)

        with open('Q&A.json', 'w') as f:
            json.dump(data, f)


        with open('Q&A.json') as f:
            data = json.load(f)
            t2s(json.dumps(data[command], indent=4, sort_keys=True))
        exit(0)
        # if the answer is not in the dictionary it should google here

main()
search()
