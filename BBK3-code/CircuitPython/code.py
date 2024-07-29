"""
# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from rainbowio import colorwheel
import neopixel

NUMPIXELS = 5  # Update this to match the number of LEDs.
SPEED = 0.05  # Increase to slow down the rainbow. Decrease to speed it up.
BRIGHTNESS = 0.2  # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.
PIN = board.D0  # This is the default pin on the 5x5 NeoPixel Grid BFF.

pixels = neopixel.NeoPixel(PIN, NUMPIXELS, brightness=BRIGHTNESS, auto_write=False)


def rainbow_cycle(wait):
    for color in range(255):
        for pixel in range(len(pixels)):  # pylint: disable=consider-using-enumerate
            pixel_index = (pixel * 256 // len(pixels)) + color * 5
            pixels[pixel] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    rainbow_cycle(SPEED)
"""


# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Digital In Out example"""
"""
import time
import board
from digitalio import DigitalInOut, Direction, Pull

# LED setup.
led = DigitalInOut(board.LED)
# For QT Py M0. QT Py M0 does not have a D13 LED, so you can connect an external LED instead.
# led = DigitalInOut(board.SCK)
led.direction = Direction.OUTPUT

# For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express, QT Py M0
switch = DigitalInOut(board.D2)
# switch = DigitalInOut(board.D5)  # For Feather M0 Express, Feather M4 Express
# switch = DigitalInOut(board.D7)  # For Circuit Playground Express
switch.direction = Direction.INPUT
switch.pull = Pull.UP

while True:
    # We could also do "led.value = not switch.value"!
    if switch.value:
        led.value = False
        print("False")
    else:
        led.value = True
        print("True")

    time.sleep(0.01)  # debounce delay
"""



# SPDX-FileCopyrightText: 2023 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""NeoKey Breakout NeoPixel Rainbow Cycle Demo"""
"""
import time
import board
import keypad
import neopixel
from rainbowio import colorwheel

# --- CONFIGURATION ---
# NeoPixel brightness. Must be a float or integer between 0.0 and 1.0, where 0 is off and
# 1 is maximum brightness. Defaults to 0.3.
BRIGHTNESS = 0.3

PIXEL_PIN = board.D0
KEY_PINS = (
    board.D1,
    board.D2,
    board.D3,
    board.D4,
    board.D5
)

# --- SETUP AND CODE ---
# Number of NeoPixels. This will always match the number of breakouts and
# therefore the number of key pins listed.
NUM_PIXELS = len(KEY_PINS)

# Create NeoPixel object.
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)

# Create keypad object.
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

# Create two lists.
# The `pressed` list is used to track the key press state.
pressed = [False] * NUM_PIXELS
# The `color_value` list is used to track the current color value for a specific NeoPixel.
color_value = [0] * NUM_PIXELS

while True:
    # Begin getting key events.
    event = keys.events.get()
    if event:
        # Remember the last state of the key when pressed.
        pressed[event.key_number] = event.pressed

    # Advance the rainbow for the key that is currently pressed.
    for index in range(NUM_PIXELS):
        if pressed[index]:
            # Increase the color value by 1.
            color_value[index] += 1
            # Set the pixel color to the current color value.
            pixels[index] = colorwheel(color_value[index])

    time.sleep(0.01)
"""


# SPDX-FileCopyrightText: Copyright (c) 2021 John Park for Adafruit
#
# SPDX-License-Identifier: MIT
# Deco Keypad
"""

import time
import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import neopixel

print("- Deco Keypad -")
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

#  ----- Keymap -----  #
# change as needed, e.g. capital A (Keycode.SHIFT, Keycode.A)
switch_a_output = Keycode.A
switch_b_output = Keycode.W
switch_c_output = Keycode.D
switch_d_output = Keycode.S
switch_e_output = Keycode.N

#  ----- Keyboard setup -----  #
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# ----- Key setup ----- #
switch_a_in = DigitalInOut(board.D1)
switch_b_in = DigitalInOut(board.D2)
switch_c_in = DigitalInOut(board.D3)
switch_d_in = DigitalInOut(board.D4)
switch_e_in = DigitalInOut(board.D5)

switch_a_in.pull = Pull.UP
switch_b_in.pull = Pull.UP
switch_c_in.pull = Pull.UP
switch_d_in.pull = Pull.UP
switch_e_in.pull = Pull.UP

switch_a = Debouncer(switch_a_in)
switch_b = Debouncer(switch_b_in)
switch_c = Debouncer(switch_c_in)
switch_d = Debouncer(switch_d_in)
switch_e = Debouncer(switch_e_in)

# ----- NeoPixel setup ----- #
MAGENTA = 0xFF00FF
CYAN = 0x0088DD
WHITE = 0xCCCCCC
BLACK = 0x000000

pixel_pin = board.D0
pixels = neopixel.NeoPixel(pixel_pin, 5, brightness=0.25)
pixels.fill(BLACK)
time.sleep(0.3)
pixels.fill(WHITE)
time.sleep(0.3)
pixels.fill(BLACK)
time.sleep(0.3)
pixels[0] = MAGENTA
pixels[1] = CYAN
pixels[2] = MAGENTA
pixels[3] = CYAN
pixels[4] = MAGENTA

while True:
    switch_a.update()  # Debouncer checks for changes in switch state
    switch_b.update()
    switch_c.update()
    switch_d.update()
    switch_e.update()

    if switch_a.fell:
        keyboard.press(switch_a_output)
        pixels[0] = WHITE
    if switch_a.rose:
        keyboard.release(switch_a_output)
        pixels[0] = MAGENTA

    if switch_b.fell:
        keyboard.press(switch_b_output)
        pixels[1] = WHITE
    if switch_b.rose:
        keyboard.release(switch_b_output)
        pixels[1] = CYAN

    if switch_c.fell:
        keyboard.press(switch_c_output)
        pixels[2] = WHITE
    if switch_c.rose:
        keyboard.release(switch_c_output)
        pixels[2] = MAGENTA

    if switch_d.fell:
        keyboard.press(switch_d_output)
        pixels[3] = WHITE
    if switch_d.rose:
        keyboard.release(switch_d_output)
        pixels[3] = CYAN

    if switch_e.fell:
        keyboard.press(switch_e_output)
        pixels[4] = WHITE
    if switch_e.rose:
        keyboard.release(switch_e_output)
        pixels[4] = MAGENTA
"""
import time
import board
import math
import random
from joystick_xl.inputs import Axis, Button, VirtualInput
from joystick_xl.joystick import Joystick
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer
import neopixel
import usb_hid
from board import IMU_PWR, IMU_SCL, IMU_SDA
from busio import I2C
from digitalio import DigitalInOut, Direction, Pull
from time import sleep

MAGENTA = 0xFF00FF
CYAN = 0x0088DD
WHITE = 0xCCCCCC
BLACK = 0x000000
gyro_x = 0.0
gyro_y = 0.0
gyro_z = 0.0
accel_x = 0.0
accel_y = 0.0
accel_z = 0.0

pixel_pin = board.D0
pixels = neopixel.NeoPixel(pixel_pin, 5, brightness=0.25)
pixels.fill(BLACK)
time.sleep(0.3)
pixels.fill(WHITE)
time.sleep(0.3)
pixels.fill(BLACK)
time.sleep(0.3)
pixelColors = [MAGENTA, CYAN, MAGENTA, CYAN, MAGENTA]
#keycodes with if currently pressed
keys = [[Keycode.W, False],[Keycode.A,False],[Keycode.S,False],[Keycode.D,False],[Keycode.N,False]]
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
#countdown = 5000
#prev_all_pressed = False
#keyboard_mode = False
#just_switched = False
#still_holding_all = False

joystick = Joystick()

from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

# Customize the device behavior here
DEVICE_NAME = "XIAO nRF52840 Sense"
INTERVAL = 0.1
SENSITIVITY = 0.01

# Turn on IMU and wait 50 ms
imu_pwr = DigitalInOut(IMU_PWR)
imu_pwr.direction = Direction.OUTPUT
imu_pwr.value = True
sleep(0.05)

# Set up I2C bus and initialize IMU
i2c_bus = I2C(IMU_SCL, IMU_SDA)
sensor = LSM6DS3(i2c_bus)

#Joystick descriptor
#If you want to add button/hat switches/axis, add a new line and add the source between parenthesis
joystick.add_input(
    Button(board.D1),
    Button(board.D2),
    Button(board.D3),
    Button(board.D4),
    Button(board.D5),
    Axis(source=VirtualInput(value=32768)),
    Axis(source=VirtualInput(value=32768)),
    Axis(source=VirtualInput(value=32768)),
    Axis(source=VirtualInput(value=32768)),
    Axis(source=VirtualInput(value=32768)),
    Axis(source=VirtualInput(value=32768)),
)

for i in range(len(pixelColors)):
    print(i)
    pixels[i] = pixelColors[i]

#turns the sensor readings into values that can be sent through joystick inputs (integer between 0 and 65535 included)
def input_processing_for_axis(analogValue: float) -> int:
    new_value = 32768 + math.floor(analogValue * 5000)
    return new_value

while True:
    #get the gyroscope and accelerometer values
    gyro_x, gyro_y, gyro_z = sensor.gyro
    accel_x, accel_y, accel_z = sensor.acceleration

    #manually updating the joystick values
    joystick.axis[0].source_value = input_processing_for_axis(gyro_y)
    joystick.axis[1].source_value = input_processing_for_axis(gyro_x)
    joystick.axis[2].source_value = input_processing_for_axis(gyro_z)
    joystick.axis[3].source_value = input_processing_for_axis(accel_y/5)
    joystick.axis[4].source_value = input_processing_for_axis(accel_x/5)
    joystick.axis[5].source_value = input_processing_for_axis(accel_z/5)
    joystick.update()

    button_pressed = 0
    for a, button in enumerate(joystick.button):
        if button.is_pressed:
            pixels[a] = WHITE
            button_pressed += 1
            #if keyboard_mode and not just_switched:
            keyboard.press(keys[a][0])
            keys[a][1] = True
        else:
            #still_holding_all = False
            if keys[a][1]:
                keyboard.release(keys[a][0])
                pixels[a] = pixelColors[a]
                keys[a][1] = False
"""
    if button_pressed == 5 and just_switched == False:
        countdown -= 10
        still_holding_all = True
        prev_all_pressed = True
        if countdown <= 0:
            keyboard_mode = not keyboard_mode
            pixels.fill(BLACK)
            just_switched = True
    elif prev_all_pressed == True and still_holding_all == False:
        prev_all_pressed = False
        just_switched = False
        countdown = 5000
"""
"""
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

i2c = board.I2C()  # uses board.SCL and board.SDA
sox = LSM6DSOX(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(sox.gyro))
    print("")
    time.sleep(0.5)
"""
"""
from _bleio import adapter
from board import IMU_PWR, IMU_SCL, IMU_SDA
from busio import I2C
from digitalio import DigitalInOut, Direction
from time import sleep

from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

# Customize the device behavior here
DEVICE_NAME = "XIAO nRF52840 Sense"
INTERVAL = 0.1
SENSITIVITY = 0.01

# Turn on IMU and wait 50 ms
imu_pwr = DigitalInOut(IMU_PWR)
imu_pwr.direction = Direction.OUTPUT
imu_pwr.value = True
sleep(0.05)

# Set up I2C bus and initialize IMU
i2c_bus = I2C(IMU_SCL, IMU_SDA)
sensor = LSM6DS3(i2c_bus)


class BTHomeAdvertisement:
    _ADV_FLAGS = [0x02, 0x01, 0x06]
    _ADV_SVC_DATA = [0x06, 0x16, 0xD2, 0xFC, 0x40, 0x22, 0x00]

    def _name2adv(self, local_name):
        adv_element = bytearray([len(local_name) + 1, 0x09])
        adv_element.extend(bytes(local_name, "utf-8"))
        return adv_element

    def __init__(self, local_name=None):
        if local_name:
            self.adv_local_name = self._name2adv(local_name)
        else:
            self.adv_local_name = self._name2adv(adapter.name)

    def adv_data(self, movement):
        adv_data = bytearray(self._ADV_FLAGS)
        adv_svc_data = bytearray(self._ADV_SVC_DATA)
        adv_svc_data[-1] = movement
        adv_data.extend(adv_svc_data)
        adv_data.extend(self.adv_local_name)
        return adv_data


bthome = BTHomeAdvertisement(DEVICE_NAME)

while True:
    #gyro_x, gyro_y, gyro_z = sensor.gyro
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(sensor.gyro))

    moving = gyro_x**2 + gyro_y**2 + gyro_z**2
    if moving > SENSITIVITY:
        print("Moving")
        adv_data = bthome.adv_data(1)
    else:
        adv_data = bthome.adv_data(0)
    adapter.start_advertising(
        adv_data, scan_response=None, connectable=False, interval=INTERVAL * 2
    )
    sleep(INTERVAL)
    #adapter.stop_advertising()
"""
