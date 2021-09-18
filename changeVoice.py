import pyttsx3
import communicate
import listen
import programExit
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def vChange(turn):
    if(turn >= len(voices)):
        communicate.speak("No more voices left. Do you want to try again?")
        programExit.pExit()
    else:
        turn+=1
        communicate.setValueID(turn)
        communicate.speak("Do you like this voice?")
        engine.setProperty('voice', voices[turn].id)
        command = listen.startListening()
        if ('yes' in command):
            communicate.speak("I love my new voice. Thank you, Shifat.")
            print("Updating Voice Information")
            communicate.setValueID(turn)
            programExit.pExit()
        else:
            vChange(turn) 



    