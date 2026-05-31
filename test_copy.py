import time
import pyperclip
from pynput.keyboard import Controller, Key

kb = Controller()

# Save old clipboard
pyperclip.copy("OLD_TEXT")
print("Clipboard set to OLD_TEXT. Please select some text in the next 3 seconds...")
time.sleep(3)

print("Sending Cmd+C...")
with kb.pressed(Key.cmd):
    kb.press('c')
    kb.release('c')

time.sleep(1)
print(f"Clipboard is now: {pyperclip.paste()}")
