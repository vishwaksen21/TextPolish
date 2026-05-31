#!/usr/bin/env python3
"""
TextPolish Paste Pipeline Diagnostic
======================================
Run this INSIDE the packaged app context (copy to the same folder as TextPolish.app/Contents/MacOS/)
or run directly with the venv python to compare.

Usage:
    source .venv/bin/activate
    python scratch/diag_paste_pipeline.py

It will:
  1. Sleep 3 seconds (switch to Chrome or another app during this time)
  2. Record what app is frontmost
  3. Simulate AppKit focus restore (the same way paste_text() does it)
  4. Record what app is frontmost AFTER restore
  5. Send Cmd+V via pynput (packaged mode path)
  6. Send Cmd+V via osascript (dev mode path)
  7. Print all results so you can compare what actually got focus

This provides PROOF of which application receives the paste event.
"""

import sys
import time
import subprocess

print("=" * 60)
print(f"Python executable: {sys.executable}")
print(f"sys.frozen (packaged): {getattr(sys, 'frozen', False)}")
print("=" * 60)

def get_frontmost():
    try:
        from AppKit import NSWorkspace
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        if app:
            bid = app.bundleIdentifier() or "Unknown"
            name = app.localizedName() or "Unknown"
            is_active = app.isActive()
            return {"bundle_id": bid, "name": name, "is_active": is_active}
    except Exception as e:
        return {"error": str(e)}
    return {}

def get_frontmost_osascript():
    try:
        res = subprocess.run(
            ['osascript', '-e',
             'tell application "System Events" to get name of first process whose frontmost is true'],
            capture_output=True, text=True, timeout=2
        )
        return res.stdout.strip() if res.returncode == 0 else f"ERROR: {res.stderr.strip()}"
    except Exception as e:
        return f"EXCEPTION: {e}"

print("\n[STEP 1] Giving you 4 seconds to switch to Chrome (or any target app)...")
for i in range(4, 0, -1):
    print(f"  Switch now... {i}")
    time.sleep(1)

print("\n[STEP 2] Recording frontmost app BEFORE any focus manipulation:")
before_appkit = get_frontmost()
before_osascript = get_frontmost_osascript()
print(f"  AppKit says:    name={before_appkit.get('name')}  bundle={before_appkit.get('bundle_id')}  is_active={before_appkit.get('is_active')}")
print(f"  osascript says: {before_osascript}")

target_bundle = before_appkit.get('bundle_id')
print(f"\n[STEP 3] Will restore focus to bundle: {target_bundle}")

# --- Simulate what paste_text() does ---
restore_success = False
if target_bundle and target_bundle != "Unknown":
    try:
        from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
        apps = NSWorkspace.sharedWorkspace().runningApplications()
        for app in apps:
            if app.bundleIdentifier() == target_bundle:
                restore_success = app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
                print(f"\n[STEP 4] activateWithOptions_ returned: {restore_success}")
                break
        
        # This is the BLOCKING call that freezes the Qt event loop in packaged mode
        print("  Sleeping 0.35s (this blocks the Qt main thread in packaged mode)...")
        time.sleep(0.35)
    except Exception as e:
        print(f"  activateWithOptions_ FAILED: {e}")
else:
    print("  No valid bundle ID to restore to.")

print("\n[STEP 5] Recording frontmost app AFTER focus restore (BEFORE paste):")
after_appkit = get_frontmost()
after_osascript = get_frontmost_osascript()
print(f"  AppKit says:    name={after_appkit.get('name')}  bundle={after_appkit.get('bundle_id')}  is_active={after_appkit.get('is_active')}")
print(f"  osascript says: {after_osascript}")

# Determine if focus was actually returned
focus_returned = (after_appkit.get('bundle_id') == target_bundle)
print(f"\n[RESULT] Focus returned to target: {focus_returned}")
if not focus_returned:
    print(f"  EXPECTED: {target_bundle}")
    print(f"  GOT:      {after_appkit.get('bundle_id')}")
    print("  *** FOCUS WAS NOT ACTUALLY RETURNED TO TARGET APP ***")
else:
    print(f"  ✓ {after_appkit.get('name')} is now frontmost.")

print("\n[STEP 6] Setting clipboard to test content...")
import pyperclip
pyperclip.copy("TEXTPOLISH_PASTE_TEST_VALUE")
time.sleep(0.1)

print("\n[STEP 7] Sending Cmd+V via pynput (packaged mode path)...")
print("         Watch what happens in the frontmost app...")
time.sleep(0.5)

try:
    from pynput.keyboard import Controller, Key
    kb = Controller()
    kb.release(Key.ctrl)
    kb.release(Key.shift)
    kb.release(Key.alt)
    kb.release(Key.cmd)
    with kb.pressed(Key.cmd):
        kb.press('v')
        kb.release('v')
    print("  pynput Cmd+V sent.")
except Exception as e:
    print(f"  pynput FAILED: {e}")

time.sleep(1.0)

print("\n[STEP 8] Sending Cmd+V via osascript (dev mode path)...")
try:
    res = subprocess.run(
        ['osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'],
        capture_output=True, text=True, timeout=3
    )
    if res.returncode == 0:
        print("  osascript Cmd+V sent successfully.")
    else:
        print(f"  osascript FAILED (rc={res.returncode}): {res.stderr.strip()}")
except Exception as e:
    print(f"  osascript EXCEPTION: {e}")

time.sleep(0.5)

print("\n[STEP 9] Final frontmost app check:")
final = get_frontmost()
final_osc = get_frontmost_osascript()
print(f"  AppKit says:    name={final.get('name')}  bundle={final.get('bundle_id')}")
print(f"  osascript says: {final_osc}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print(f"Target bundle was:    {target_bundle}")
print(f"Focus after restore:  {after_appkit.get('bundle_id')}")
print(f"Focus returned:       {focus_returned}")
print(f"restore_success API:  {restore_success}")
print()
print("KEY QUESTION: Did you see 'TEXTPOLISH_PASTE_TEST_VALUE'")
print("pasted into Chrome after Step 7 (pynput)?")
print("Or only after Step 8 (osascript)?")
print("Or neither?")
