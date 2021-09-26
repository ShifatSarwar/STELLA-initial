import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageSequence 
from PySimpleGUI.PySimpleGUI import TITLEBAR_MINIMIZE_KEY, Titlebar, popup_animated

sg.theme('DarkAmber')
gif_filename = r'shapeB.gif'

layout = [[ 
    [sg.Image(filename=gif_filename,
              enable_events=True,
              key="-IMAGE-")],

]]

# Create the Window
window = sg.Window('STELLA', layout, finalize=True) 
# Event Loop to process "events" and get the "values" of the inputs
while True:
    for frame in ImageSequence.Iterator(Image.open(gif_filename)):
        event, values = window.read(timeout=65)
        window['-IMAGE-'].update(data=ImageTk.PhotoImage(frame) )
    if event == sg.WIN_CLOSED : # if user closes window or clicks cancel
        break
window.close()
