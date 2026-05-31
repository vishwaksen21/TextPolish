import subprocess
import time
import pyperclip

pyperclip.copy("OLD_TEXT")
print("Sending Cmd+A and Cmd+C via osascript...")

script = '''
tell application "System Events"
    keystroke "a" using command down
    delay 0.5
    keystroke "c" using command down
end tell
'''
result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print("rc:", result.returncode)
print("err:", result.stderr)
time.sleep(1)
print(f"Clipboard is now: {pyperclip.paste()}")
