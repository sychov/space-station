@echo off
"C:\Program Files\7-Zip"\7z.exe a .\dist\space_station.zip .\dist\space_station
rmdir /s /q build
rmdir /s /q .\dist\space_station