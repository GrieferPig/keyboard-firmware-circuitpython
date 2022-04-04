# DO NOT USE THIS PROGRAM DIRECTILY WITHOUT MODIFICAION - IT WILL NOT WORK

# code.py
# A simple program that detects keys on a matrix keyboard and press them via HID interface.
# Author: GrieferPig
# Date: 4/4/2022

# include libs
import time
import board as b
from adafruit_hid.keycode import Keycode as k # alias for quicker and cleaner coding
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize key map
# Suppose we divide the keyboard as lines and columns
# Each 2-dimentional array is a line
# The first array's data (e.g. b.GP16) represents where the line's pin corresponding to gpio. Let's call it the Main Bus.
# The second array is potential keys that can activate the "Main Bus" with corresponding keys. Call it other keys.
# The third array is keycode that corresponds to other keys previously. **PLACED IN ORDER**
# The last array is the function key if it can trigger other key with fn key pressed. **PLACED IN ORDER**
# If there are keys that don't have a fn function, leave it "" (empty string)
# For example, there is a key that connected to GP16 and GP3 labeled as "W" and it's also F1 key, then the array would look like this: [[b.GP16],[3],[k.W],[k.F1]]

p17=[[b.GP16],[3,4,7,8,9,11],[k.LEFT_CONTROL,k.GRAVE_ACCENT,k.FIVE,k.SIX,k.EQUALS,k.MINUS],[]]
p18=[[b.GP17],[4,5,6,7,8,9,10,11],[k.ONE,k.TWO,k.THREE,k.FOUR,k.SEVEN,k.EIGHT,k.NINE,k.ZERO],[]]
p19=[[b.GP18],[4,5,6,7,8,9,10,11],[k.Q,k.W,k.E,k.R,k.O,k.I,k.U,k.P]]
p20=[[b.GP19],[1,2,4,5,7,8,9,11,13],[k.OPTION,k.LEFT_SHIFT,k.TAB,k.CAPS_LOCK,k.T,k.Y,k.BACKSLASH,k.FORWARD_SLASH,k.BACKSPACE],[]]
p22=[[b.GP20],[0,4,5,6,7,8,9,10,11],[k.GUI,k.A,k.S,k.D,k.F,k.J,k.K,k.L,k.ENTER],[]]
p23=[[b.GP21],[4,5,6,8,9,10,11,13],[k.Z,k.X,k.C,k.N,k.M,k.COMMA,k.SEMICOLON,k.RIGHT_SHIFT],[]]
p24=[[b.GP22],[0,7,8,12,14],[k.COMMAND,k.G,k.H,k.UP_ARROW,k.SPACE],[]]
p25=[[b.GP26],[7,8,11,12,14,15],[k.V,k.B,k.PERIOD,k.LEFT_ARROW,k.DOWN_ARROW,k.RIGHT_ARROW],[]]

# Put these main buses together for looping
pins = [p17,p18,p19,p20,p22,p23,p24,p25]

# Here is your "other keys". Note that they cannot be duplicated.
other_pins_unrepeated = [b.GP0,b.GP1,b.GP2,b.GP3,b.GP4,b.GP5,b.GP6,b.GP7,b.GP8,b.GP9,b.GP10,b.GP11,b.GP12,b.GP13,b.GP14,b.GP15]

# set all test pins pull down
for pin in pins:
    key_pin = digitalio.DigitalInOut(pin[0][0])
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.DOWN
    pin[0][0]=key_pin

# set all other pins ready
for pin in other_pins_unrepeated:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.OUTPUT
    key_pin.value = False
    other_pins_unrepeated[other_pins_unrepeated.index(pin)]=key_pin

# replace other keys in pins array with set keys (shallow copy)
for pin in pins:
    for key_pin in pin[1]:
        pin[1][pin[1].index(key_pin)] = other_pins_unrepeated[key_pin]
        
press_record = [] # recording previous pressed button record
fn = false # if fn is pressed then true

# init
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

print("ready.")

# 'Mane' loop finally
while True:
    for pin in pins:
        for _other in pin[1]:
            _other.value=True
            _key_name=pin[2][pin[1].index(_other)]
            if pin[0][0].value == True:
                if not _key_name in press_record:
                    press_record.append(_key_name)
                    keyboard.press(pin[2][pin[1].index(_other)]) # press
            else:
                if _key_name in press_record:
                    press_record.remove(_key_name)
                    keyboard.release(pin[2][pin[1].index(_other)]) # release
            _other.value=False
