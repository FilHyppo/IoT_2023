import serial

try:
    serialport = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=4)  # cambiare valore porta in bse a quella scelta
    #per arduino, su windows è COMx dove x è un intero (es. COM6)
except serial.SerialException as e:
    print(f"Errore nell'apertura della porta seriale: {e}")
    exit()

while True:
    try:
        arduinoData = serialport.readline().decode('ascii')
        print(arduinoData)
    except serial.SerialException as e:
        print(f"Errore durante la lettura dalla porta seriale: {e}")
