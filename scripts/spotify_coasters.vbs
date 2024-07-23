' This script is designed to run the Python script spotify_coasters.py on startup on your Windows machine. Replace the
' variable scriptPath in the code below with the full path to your spotify_coasters.py script. You can then comment out
' the script below. Be careful when running this script as it will run as a background process. Move this script to the
' Windows startup folder to have the script ran during startup. You can find the location of your startup folder by
' typing "WindowsKey + R" and entering "shell:startup".

' Dim scriptPath: scriptPath = "C:/Change/Path/spotifycoasters/scripts/spotify_coasters.py"
' Dim oShell
' Set oShell = WScript.CreateObject ("WSCript.shell")
' Call oShell.Run("cmd /K python """ & scriptPath & """", 0, True)
' Set oShell = Nothing