import os

os.system('arduino-cli compile -b arduino:avr:mega /Users/abdullahimohammed/Documents/Arduino/CurrentAndVoltageTest_29Mar')
os.system('arduino-cli upload -b arduino:avr:mega -p /dev/cu.usbmodem14101 /Users/abdullahimohammed/Documents/Arduino/CurrentAndVoltageTest_29Mar')
