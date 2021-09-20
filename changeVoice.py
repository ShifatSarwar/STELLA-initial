import pyttsx3
import communicate
import listen
import programExit
engine = pyttsx3.init()
voices = engine.getProperty('voices')

#This code basically runs until user confirms a voice thorugh command

def vChange():
    turn = communicate.getValueID()
    #turn will start from the turn in file
    if(turn >= len(voices)):
        turn=0
    else:
        turn+=1
        communicate.setValueID(turn)
        communicate.speak("Do you like this voice?")
        engine.setProperty('voice', voices[turn].id)
        command = listen.startListening()
        #confirm voice
        if ('yes' in command):
            communicate.speak("I love my new voice. Thank you, Shifat.")
            print("Updating Voice Information")
            communicate.setValueID(turn)
            programExit.sExit()

        else:
            vChange(turn) 



    