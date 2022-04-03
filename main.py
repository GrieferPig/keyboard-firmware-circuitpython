import time
import board as b
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

p17=[[b.GP16],[3,4,7,8,9,11],[Keycode.A,"9","10","","",""]]
p18=[[b.GP17],[4,5,6,7,8,9,10,11],["2","11","","","","","",""]]
p19=[[b.GP18],[4,5,6,7,8,9,10,11],["3","","","","","","",""]]
p20=[[b.GP19],[1,2,4,5,7,8,9,11,13],["4","","","","","","","",""]]
p22=[[b.GP20],[0,4,5,6,7,8,9,10,11],["5","","","","","","","",""]]
p26=[[b.GP21],[4,5,6,8,9,10,11,13],["6","","","","","","",""]]
p24=[[b.GP22],[0,7,8,12,14],["7","","","",""]]
p25=[[b.GP26],[7,8,11,12,14,15],["8","","","","",""]]

pins = [p17,p18,p19,p20,p22,p26,p24,p25]

other_pins_unrepeated = [b.GP0,b.GP1,b.GP2,b.GP3,b.GP4,b.GP5,b.GP6,b.GP7,b.GP8,b.GP9,b.GP10,b.GP11,b.GP12,b.GP13,b.GP14,b.GP15]

# init
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

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