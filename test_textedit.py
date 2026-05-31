import subprocess
import time
import pyperclip
from pynput.keyboard import Controller, Key

kb = Controller()

pyperclip.copy("OLD_TEXT")
print("Opening TextEdit and typing some text...")

# Open TextEdit and type something
script = '''
tell application "TextEdit"
    activate
    make new document
end tell
'''
subprocess.run(['osascript', '-e', script])
time.sleep(2)

print("Typing and selecting text...")
with kb.pressed(Key.shift):
    kb.press('a')
    kb.release('a')
time.sleep(0.5)

with kb.pressed(Key.cmd):
    kb.press('a')
    kb.release('a')
time.sleep(0.5)

print("Sending Cmd+C via pynput...")
with kb.pressed(Key.cmd):
    kb.press('c')
    kb.release('c')

time.sleep(1)
print(f"Clipboard is now: {pyperclip.paste()}")

# Clean up TextEdit
script2 = '''
tell application "TextEdit"
    close front document saving no
end tell
'''
subprocess.run(['osascript', '-e', script2])
