#!/usr/bin/env python
from torch.nn.modules.activation import Softmax
from functions.listen import startListening
from functions.communicate import speak
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageSequence 
from functions.calculations import addition, subtraction, division, multiplication, tothePower, percentages
#from functions.changeVoice import vChange
from functions.variousSearch import googleSearch, play, findInfo, chooseGenre
import datetime
import random
from functions.readFiles import pathToOpenedDoc, readFromFile
import torch
from functions.weatherService import weatherService
#from functions.programExit import pExit
import json
from training.model import NeuralNet
from training.nltkutilities import tokenize, bag_of_words
#checking import

from functions.readFiles import readFromFile

if __name__ == '__main__':

    #Allows use of cuda or cpu for computing prediction
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    #read from json data for getting responses based on asked questions
    with open('intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    #File contains model trained
    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    #Gets model up and running
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    #loads up chosen voice rather than default voice
    # setValueID(getValueID())

    # sg.theme('DarkAmber')
    # gif_filename = r'shapeB.gif'

    # layout = [[ 
    # [sg.Image(filename=gif_filename,
    #           enable_events=True,
    #           key="-IMAGE-")],
    # ]]

    # # Create the Window
    # window = sg.Window('STELLA', layout, finalize=True) 
    
    #listening starts here
    #readFromFile()
    while True:
        command = startListening()
        # for frame in ImageSequence.Iterator(Image.open(gif_filename)):
        #     event, values = window.read(timeout=10)
        #     window['-IMAGE-'].update(data=ImageTk.PhotoImage(frame) )
        if 'exit' in command or 'go away' in command:
            break

        # elif('change voice' in command):
        #     vChange()

        elif('time' in command):
            time = datetime.datetime.now().strftime('%I:%M:%p')
            speak("The current time is, " + time)
        elif('read' in command):
            path = pathToOpenedDoc()
            index = 0
            speak(readFromFile(path, 0))
            while True:      
                command = startListening()
                if 'stop' in command:
                    break
                elif 'next' in command:
                    index+=1
                    speak(readFromFile(path, index))
        else:
            #convert command into a tokenized array
            command = tokenize(command)

            #get arrays to compare and predict
            X = bag_of_words(command, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted  = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            #runs if probability high
            if prob.item() > 0.75 :
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        response = random.choice(intent["responses"])
                        if tag == "youtube":
                            #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                tokenizeTokens = tokenize(tokens)
                                for t in tokenizeTokens:
                                    if t in command:
                                        command.remove(tokens)
                            videoTitle = ' '.join(command)
                            speak(response+videoTitle)
                            play(videoTitle)

                        elif tag == "weather":
                            #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                tokenizeTokens = tokenize(tokens)
                                for t in tokenizeTokens:
                                    if t in command:
                                        command.remove(t)
                                print(command)
                            weatherCity = ' '.join(command)
                            print(weatherCity)
                            print(weatherCity)
                            speak(weatherService().get_weather_data(weatherCity))

                        elif tag == 'search':
                        #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            search = ' '.join(command)
                            speak(response+search)
                            googleSearch(search)

                        elif tag == 'info':
                        #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            searchInfo = ' '.join(command)
                            speak(response)
                            speak(findInfo(searchInfo))

                        #calculations
                        elif tag == 'add':
                            searchInfo =' '.join(command)
                            speak(response+addition(searchInfo))
                        
                        elif tag == 'subtract':
                            searchInfo =' '.join(command)
                            speak(response+subtraction(searchInfo))
                        
                        elif tag == 'multiply':
                            searchInfo =' '.join(command)
                            speak(response+multiplication(searchInfo))
                        
                        elif tag == 'divide':
                            searchInfo =' '.join(command)
                            speak(response+division(searchInfo))
                        
                        elif tag == 'percent':
                            searchInfo =' '.join(command)
                            speak(response+percentages(searchInfo))
                        
                        elif tag == 'power':
                            searchInfo =' '.join(command)
                            speak(response+tothePower(searchInfo))
                        
                        elif tag == 'suggest':
                            speak("Sorry, that is not available yet")

                        else:
                            #A response generated by AI
                            speak(response)
                             
            else:
                #response if user talks jibberish
                speak("Sorry, could not understand you")

    quit()
  
        






