tell application "System Events"
    set theApp to first application process whose frontmost is true
    set theElement to focused UI element of theApp
    return value of attribute "AXSelectedText" of theElement
end tell
