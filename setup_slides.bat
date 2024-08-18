@echo off
setlocal

:: Create the slides directory if it doesn't exist
if not exist slides (
    mkdir slides
)

:: Create the Cheat Sheet file
echo Appointments: > slides\cheat_sheet.txt

echo. >> slides\cheat_sheet.txt
echo Upcoming Courses: >> slides\cheat_sheet.txt


echo Cheat sheet has been created successfully.
pause
endlocal
