#!/usr/bin/env python3
import serial
from pynput.keyboard import Controller, Key

# 1️⃣ Open port with short timeout
ser = serial.Serial('/dev/cu.usbmodemV1_0_9c6d1', 9600, timeout=0.1)

# 2️⃣ Set up the keyboard controller
keyboard = Controller()

while True:
    raw = ser.readline()                    # grab full scan (to NL/CR)
    if not raw:
        continue

    chunk = raw.rstrip(b'\r\n')
    if not chunk:
        continue

    # 3️⃣ Map control codes → placeholders
    out = []
    for b in chunk:
        if   b == 0x1E: out.append('<RS>')
        elif b == 0x1D: out.append('<GS>')
        elif b == 0x04: out.append('<EOT>')
        else:           out.append(chr(b))
    text = ''.join(out)

    # 4️⃣ Type it all at once, then hit Enter
    keyboard.type(text)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
