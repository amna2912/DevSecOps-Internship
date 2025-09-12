@echo off
echo Installing required Python packages...
pip install flask requests pywin32

echo Downloading Fluent Bit for Windows...
powershell -Command "Invoke-WebRequest -Uri 'https://fluentbit.io/releases/2.2/fluent-bit-2.2.0-win64.zip' -OutFile 'fluent-bit.zip'"
powershell -Command "Expand-Archive -Path fluent-bit.zip -DestinationPath ."
ren fluent-bit-2.2.0-win64 fluent-bit
del fluent-bit.zip

echo Setup complete!
pause