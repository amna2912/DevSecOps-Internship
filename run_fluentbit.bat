@echo off
echo Starting Fluent Bit...
cd fluent-bit\bin
fluent-bit.exe -c ..\..\fluent-bit.conf
pause
