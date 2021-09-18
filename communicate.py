import pyttsx3
engine = pyttsx3.init()

def speak(command):
    print(command)
    engine.say(command)
    engine.runAndWait()

def getValueID():
    with open('requirements.txt') as f:
        lines = f.readlines()
        for line in lines:
            listval=line.split()
            return int(listval[2])

def setValueID(turn):
    voices = engine.getProperty('voices')
    infoFile = open("requirements.txt", "r")
    list_of_lines = infoFile.readlines()
    list_of_lines[0] = "idValue = "+str(turn)
    infofFile = open("requirements.txt", "w")
    infofFile.writelines(list_of_lines)
    infofFile.close()
    engine.setProperty('voice', voices[getValueID()].id)


