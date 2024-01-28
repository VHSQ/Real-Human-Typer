import customtkinter as ctk
import json
import pyautogui
import keyboard
import pyperclip
import time
from threading import Thread

# Load settings from settings.json file
with open('settings.json', 'r') as file:
    settings = json.load(file)

typing_active = False  # Typing state is initially inactive
text = ""  # Initialize text
index = 0  # Initialize index

def type_text():
    global typing_active, text, index
    if index == 0:  # Get text only if starting anew
        text = text_input.get("1.0", 'end-1c')
        if not text:
            text = pyperclip.paste()

    delay = 1 / (settings['speed'] * 10 + 1)  # Calculate delay based on speed setting

    for i in range(index, len(text)):
        if not typing_active:
            break  # Stop typing if typing is no longer active
        pyautogui.write(text[i])
        time.sleep(delay)
        index = i + 1  # Update the index

def stop_typing(event=None):
    global typing_active, index
    typing_active = False

def resume_typing(event=None):
    global typing_active, index
    if not typing_active:  # Only start thread if not already typing
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
    speed_slider_label.set(f"Speed: {default_settings['speed']}")

# GUI setup
root = ctk.CTk()
root.title("Text Typer")

frame_input = ctk.CTkFrame(root)
frame_input.pack(padx=20, pady=20, fill="both", expand=True)

text_input = ctk.CTkTextbox(frame_input)
text_input.pack(padx=20, pady=20, fill="both", expand=True)

insert_button = ctk.CTkButton(root, text="Press INSERT to start", command=resume_typing)
insert_button.pack(side='left')

delete_button = ctk.CTkButton(root, text="Press DELETE to stop", command=stop_typing)
delete_button.pack(side='right')

# Bind INSERT and DELETE keys to the functions
keyboard.add_hotkey('insert', resume_typing)
keyboard.add_hotkey('delete', stop_typing)

frame_settings = ctk.CTkFrame(root)
frame_settings.pack(padx=20, pady=(0, 20), fill='x')

def update_speed_label(val):
    settings['speed'] = int(float(val))
    speed_slider_label.set(f"Speed: {int(val)}") # Use set method and cast val to int

speed_slider_label = ctk.CTkLabel(frame_settings, text=f"Speed: {settings['speed']}")
speed_slider_label.grid(column=0, row=0, padx=(10))

speed_slider = ctk.CTkSlider(frame_settings, from_=0, to=50, command=update_speed_label)
speed_slider.set(settings['speed'])
speed_slider.grid(column=1, row=0, padx=(10))

save_button = ctk.CTkButton(frame_settings, text="Save Settings", command=save_settings)
save_button.grid(column=2, row=0, padx=(10))

reset_button = ctk.CTkButton(frame_settings, text="Reset To Default", command=reset_to_default)
reset_button.grid(column=3, row=0, padx=(10))

# Add a reset button and bind the END key to it
def reset_text(event=None):
    global typing_active, text, index
    text_input.delete("1.0", "end") # Clear the text input
    index = 0 # Reset the index
    typing_active = False # Set the typing state to false

reset_button = ctk.CTkButton(frame_settings, text="Reset", command=reset_text) # Create a reset button
reset_button.grid(column=4, row=0, padx=(10)) # Add the reset button to the grid

keyboard.add_hotkey('end', reset_text) # Bind the END key to the reset function

root.mainloop()
