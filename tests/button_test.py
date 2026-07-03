import os
from gpiozero import Button
from signal import pause

# 1. Initialize the buttons with internal pull-up resistors
# This matches the physical ground-wired breadboard setup
btn_display_1 = Button(16)
btn_display_2 = Button(22)
btn_display_3 = Button(23)
btn_display_4 = Button(27)
btn_volume_up = Button(20, pull_up=True, bounce_time=0.05)
btn_volume_down = Button(26, pull_up=True, bounce_time=0.05)

# 2. Define the Volume Control functions (using system ALSA commands)
def increase_volume():
    print("Volume Up Pressed")
    # Increases Master volume by 5% increments
    os.system("amixer set Master 5%+")

def decrease_volume():
    print("Volume Down Pressed")
    # Decreases Master volume by 5% increments
    os.system("amixer set Master 5%-")

# 3. Define the Rerouted Display Button function
def display_button_1_action():
    print("Display Button 1 (Rerouted to GPIO 16) Pressed!")
    # Insert your UI / screen toggle script action here

def display_button_2_action():
    print("Display Button 2 Pressed!")
    # Insert your UI / screen toggle script action here

def display_button_3_action():
    print("Display Button 3 Pressed!")

    # Insert your UI / screen toggle script action here
def display_button_4_action():
    print("Display Button 4 Pressed!")
    # Insert your UI / screen toggle script action here

# 4. Bind the physical press events to the functions
btn_display_1.when_pressed = display_button_1_action
btn_display_2.when_pressed = display_button_2_action
btn_display_3.when_pressed = display_button_3_action
btn_display_4.when_pressed = display_button_4_action
btn_volume_up.when_pressed = increase_volume
btn_volume_down.when_pressed = decrease_volume

print("--- System Map Initialized ---")
print("GPIO 16 -> Display Button 1")
print("GPIO 22 -> Display Button 2")
print("GPIO 23 -> Display Button 3")
print("GPIO 27 -> Display Button 4")
print("GPIO 20 -> Volume Up")
print("GPIO 26 -> Volume Down")
print("Listening for button presses... Press Ctrl+C to exit.")

# 5. Keep the background listener script running cleanly
pause()
