import serial
from master_obj import Master

master = Master(user={'email': 'filippo@fam.bologna.it', 'password': 'admin', 'username': 'admin'})


# Funzione che mappa il valore letto dal sensore di umidità in un valore percentuale
def percentuale(x):
    min_val = 412  # corrisponde a 100% di umidità
    max_val = 808  # corrisponde a 0% di umidità
    percentage = 100 - ((int(x) - min_val) * 100) / (max_val - min_val)

    # faccio si che il valore percentuale sia compreso tra 0 e 100 e lo porto ad una sola cifra decimale
    return round(max(0, min(percentage, 100)), 0)


try:
    serialport = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=4)  # cambiare valore porta in bse a quella scelta
    # per arduino, su windows è COMx dove x è un intero (es. COM6)
except serial.SerialException as e:
    print(f"Errore nell'apertura della porta seriale: {e}")
    exit()

while True:
    try:
        arduinoData = serialport.readline().decode('ascii')
        # print(arduinoData)

        # divide la stringa ad ogni spazio, in posizione 0 c'è la stringa 'id' e in posizione 1 c'è il valore dell'id,
        # in posizione 2 c'è la stringa 'umidita' e in posizione 3 c'è il valore dell'umidità
        parts = arduinoData.split()
        if len(parts) == 4:  # se la lunghezza della lista è 4 allora ci sono tutti i dati
            iD = parts[1]
            umidita = percentuale(parts[3])  # converto il valore dell'umidità in percentuale

            # Stampa i valori letti
            print("ID:", iD)
            print("Umidita:", umidita)
            master.inserisci_misurazione(iD, umidita)
        else:
            print("Errore: Dati mancanti dopo lo split")

    except serial.SerialException as e:
        print(f"Errore durante la lettura dalla porta seriale: {e}")
