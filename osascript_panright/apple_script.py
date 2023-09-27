

applescript_panright = """
    tell application "System Preferences"
	activate
	reveal anchor "output" of pane id "com.apple.preference.sound"
end tell
tell application "System Events"
	tell slider 1 of group 1 of tab group 1 of window 1 of process "System Preferences"
		set value to 1.0
		delay 1
		set value to -1.0
		delay 1
		set value to 0
	end tell
end tell
"""