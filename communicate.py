import pyttsx3
import random
import os
from gtts import gTTS
import playsound
engine = pyttsx3.init()

#It allows Speak rather than print out words
def speak(command):
    tts = gTTS(text=command, lang='en')
    r = random.randint(1,10000000)
    audiofile = 'audio-'+str(r) + '.mp3'
    tts.save(audiofile)
    print(command)
    playsound.playsound(audiofile)
    os.remove(audiofile)

    #engine.say(command)
    #engine.runAndWait()

#Gets value from userdata.txt about current saved voice
def getValueID():
    with open('userdata.txt') as f:
        lines = f.readlines()
        for line in lines:
            listval=line.split()
            return int(listval[2])

#Updates userdata.txt withh updated voice information
def setValueID(turn):
    voices = engine.getProperty('voices')
    infoFile = open("userdata.txt", "r")
    list_of_lines = infoFile.readlines()
    list_of_lines[0] = "idValue = "+str(turn)
    infofFile = open("userdata.txt", "w")
    infofFile.writelines(list_of_lines)
    infofFile.close()
    engine.setProperty('voice', voices[getValueID()].id)


