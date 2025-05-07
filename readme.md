# pySerialScanner

A simple Python script that reads full lines from a serial barcode scanner (or any serial device) and emulates keyboard input on macOS by sending keystrokes via AppleScript. Control codes RS (0x1E), GS (0x1D), and EOT (0x04) are mapped to human-readable placeholders (`<RS>`, `<GS>`, `<EOT>`).

---

## Features

* Reads complete scans as lines (terminated by CR/LF) to avoid splitting larger barcodes in the middle.
* Replaces embedded control bytes:

  * **RS** (`0x1E`) → `<RS>`
  * **GS** (`0x1D`) → `<GS>`
  * **EOT** (`0x04`) → `<EOT>`
* Sends the entire processed string in one AppleScript call for speed, then a Return key.
* Gracefully handles `Ctrl-C`, closing the serial port cleanly.
* Configurable via command-line arguments: serial device path, baud rate, timeout.

---

## Requirements

* **macOS** (tested on macOS 15.4.1)
* **Python 3.7+**
* [`pyserial`](https://pypi.org/project/pyserial/)

---

## Installation

1. Clone or download this repository.
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip3 install pyserial
   ```

---

## Usage

Make the script executable and run it with the path to your serial device:

```bash
chmod +x pyScanner.py
./pySerialScanner.py /dev/cu.usbmodemV1_0_9c6d1
```

By default it uses 9600 baud and a 0.1 s read timeout. You can override these:

```bash
./pySerialScanner.py /dev/tty.usbserial-1234 -b 115200 -t 0.05
```

Once running, each scan from the device will be typed into the currently focused application, followed by an Enter.

Press **Ctrl-C** to quit; the script will close the serial port and exit gracefully.

---

## macOS Accessibility

In order for the script to send keystrokes via AppleScript, you must grant your Python interpreter Accessibility permissions:

1. Open **System Preferences** → **Security & Privacy** → **Privacy** tab.
2. Select **Accessibility** from the left-hand list.
3. Click the lock and authenticate.
4. Add your `python3` binary (or the terminal app you use) to the list.

---

## Troubleshooting

* **No input appears**: Verify the scanner is appending a CR or LF suffix. Check with `screen` or `minicom`:

  ```bash
  screen /dev/cu.usbmodemV1_0_9c6d1 9600
  ```
* **Permission errors**: Ensure you’ve granted Accessibility permissions to the correct binary.
* **Port busy**: Make sure no other application is holding the serial port open.

---

## License

MIT
