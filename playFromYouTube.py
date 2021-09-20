import pywhatkit
import programExit

#currently only plays from youtube
def play(videoTitle):
    pywhatkit.playonyt(videoTitle)
    programExit.sExit()
    