import serial

# Open the serial port
ser = serial.Serial('/dev/tty.usbserial-130', baudrate=19200, timeout=1)

# Send the ID query (command for ESP300)
ser.write(b'1ID?\r')

# Read response (up to 100 bytes)
response = ser.read(100)

# Print it
print("ESP300 Response:", response.decode().strip())

# Close the port
ser.close()
