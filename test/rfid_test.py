import serial

PORT = '/dev/ttyUSB0'
RFID_LENGTH = 18
RFID_SEP = b'\r'
MIN_REP = 1

s = serial.Serial(PORT, timeout=0.01)
s.flushInput()
buffer = b''
while True:
    buffer += s.read(RFID_LENGTH)
    rfids = [
        rfid for rfid in buffer.split(RFID_SEP) if len(rfid) == RFID_LENGTH
    ]
    if len(set(rfids)) > 1:
        print('Inconsistent input')
        buffer = b''
        continue
    if len(rfids) >= MIN_REP:
        rfid = rfids[0]
        break
print(rfid)
s.close()
