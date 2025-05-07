#!/usr/bin/env python3
import argparse
import serial
import subprocess

def send_keystroke(text: str):
    """Tell macOS to type out `text`. Escape any double-quotes."""
    safe = text.replace('"', '\\"')
    cmd = f'tell application "System Events" to keystroke "{safe}"'
    subprocess.run(['osascript', '-e', cmd], check=True)

def send_return():
    """Emit a Return/Enter keypress."""
    subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to key code 36'
    ], check=True)

def main():
    p = argparse.ArgumentParser(
        description="Read full lines from a serial barcode scanner and emit keystrokes."
    )
    p.add_argument(
        'device',
        help='Serial device path, e.g. /dev/cu.usbmodemV1_0_9c6d1'
    )
    p.add_argument(
        '-b', '--baud',
        type=int,
        default=9600,
        help='Baud rate (default: 9600)'
    )
    p.add_argument(
        '-t', '--timeout',
        type=float,
        default=0.1,
        help='Read timeout in seconds (default: 0.1)'
    )
    args = p.parse_args()

    ser = serial.Serial(args.device, args.baud, timeout=args.timeout)

    print(f"Listening on {args.device} at {args.baud} baud… (Ctrl-C to quit)")

    while True:
        raw = ser.readline()            # grab up through CR or LF
        if not raw:
            continue

        chunk = raw.rstrip(b'\r\n')
        if not chunk:
            continue

        # map control codes → placeholder strings
        out = []
        for b in chunk:
            if   b == 0x1E: out.append('<RS>')
            elif b == 0x1D: out.append('<GS>')
            elif b == 0x04: out.append('<EOT>')
            else:           out.append(chr(b))
        text = ''.join(out)

        # send in one shot, then Return
        send_keystroke(text)
        send_return()

if __name__ == '__main__':
    main()
