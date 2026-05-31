import time
import pyperclip
from pynput.keyboard import Controller, Key

kb = Controller()

pyperclip.copy("OLD_TEXT")
print("Selecting all text and copying...")
time.sleep(1)

with kb.pressed(Key.cmd):
    kb.press('a')
    kb.release('a')

time.sleep(0.5)

with kb.pressed(Key.cmd):
    kb.press('c')
    kb.release('c')

time.sleep(1)
print(f"Clipboard is now: {pyperclip.paste()}")
