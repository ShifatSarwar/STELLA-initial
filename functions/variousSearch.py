import pywhatkit

#currently only plays from youtube
def play(videoTitle):
    pywhatkit.playonyt(videoTitle)


def googleSearch(search):
    pywhatkit.search(search)

def findInfo(thing):
   return pywhatkit.info(thing, return_value=True)

def chooseGenre(stuff, command):
    suggestion = "Did not understand sorry. Try Again."
    return suggestion
            
