import tkinter as tk
from tkinter import ttk
import json
import pyautogui
import keyboard
import pyperclip
import time
from threading import Thread

# Load settings from settings.json file
with open('settings.json', 'r') as file:
    settings = json.load(file)

typing_active = True  # Initialize typing state
text = ""  # Initialize text
index = 0  # Initialize index

def type_text():
    global typing_active, text, index
    text = text_input.get("1.0",'end-1c')
    delay = 1 / (settings['speed'] * 10 + 1) # Increase the speed factor by 10
    
    if not text:
        text = pyperclip.paste()

    # Resume typing from the current index
    for i in range(index, len(text)):
        if not typing_active:
            break  # Stop typing if typing is no longer active
        pyautogui.write(text[i])
        time.sleep(delay)
        index = i + 1 # Update the index

def stop_typing(event=None):
    global typing_active, index
    typing_active = False
    index = index - 1 # Adjust the index

def resume_typing(event=None):
    global typing_active, index
    typing_active = True
    t = Thread(target=type_text)
    t.start()

def save_settings():
    speed = speed_slider.get()
    settings['speed'] = speed
    
    with open('settings.json', 'w') as file:
        json.dump(settings, file)

def reset_to_default():
    with open('settings.json', 'r') as file:
        default_settings = json.load(file)
    
    speed_slider.set(default_settings['speed'])

# GUI setup
root = tk.Tk()
root.title("Text Typer")

frame_input = ttk.LabelFrame(root, text="Text Input")
frame_input.pack(padx=20, pady=20, fill="both", expand=True)

text_input = tk.Text(frame_input, wrap='word')
text_input.pack(padx=20, pady=20, fill="both", expand=True)

# Replace the start button with two buttons
insert_button = ttk.Button(root, text="Press INSERT to start", command=resume_typing)
insert_button.pack(side='left')

delete_button = ttk.Button(root, text="Press DELETE to stop", command=stop_typing)
delete_button.pack(side='right')

# Bind INSERT and DELETE keys to the functions
keyboard.add_hotkey('insert', resume_typing)
keyboard.add_hotkey('delete', stop_typing)

frame_settings = ttk.LabelFrame(root, text="Settings")
frame_settings.pack(padx=20,pady=(0,20),fill='x')

speed_slider_label = ttk.Label(frame_settings,text=f"Speed: {settings['speed']}")
speed_slider_label.grid(column=0,row=0,padx=(10))

speed_slider_value=tk.IntVar(value=settings['speed'])
def update_speed_label(val):
   speed_slider_label.config(text=f"Speed: {val}")

# Speed slider setup 
speed_slider=tk.Scale(frame_settings,
                      from_=0,to_=50, # Increase the range to 0-50
                      orient='horizontal',
                      length=300,
                      variable=speed_slider_value,
                      command=update_speed_label)
speed_slider.grid(column=1,row=0,padx=(10))

save_button = ttk.Button(frame_settings, text="Save Settings", command=save_settings)
save_button.grid(column=2,row=0,padx=(10))

reset_button = ttk.Button(frame_settings, text="Reset To Default", command=reset_to_default)
reset_button.grid(column=3,row=0,padx=(10))

root.mainloop()
