import serial
import configparser
from master_obj import Master

# Funzione per leggere l'indirizzo IP e la porta seriale dal file di configurazione
def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        ip_address = config.get("DEFAULT", "IP_ADDRESS")
        serial_port = config['DEFAULT']['SERIAL_PORT']
        return ip_address, serial_port
    except KeyError as e:
        print(f"Chiave mancante nel file di configurazione: {e}")
        exit(1)
    except Exception as e:
        print(f"Errore nel caricamento del file di configurazione: {e}")
        exit(1)


# Ottieni l'indirizzo IP e la porta seriale dalla configurazione
ip_address, serial_port = read_config()

# Crea un'istanza di Master utilizzando l'indirizzo IP letto dalla configurazione
master = Master(user={'email': 'admin@admin.admin', 'password': 'admin', 'username': 'admin'}, base_url="http://"+ip_address+":8000/api/")

# Rimani in ascolto dei dati dalla porta seriale
try:
    serialport = serial.Serial(serial_port, 9600, timeout=4)
except serial.SerialException as e:
    print(f"Errore nell'apertura della porta seriale: {e}")
    exit()

# Funzione che mappa il valore letto dal sensore di umidità in un valore percentuale
def percentuale(x):
    min_val = 412  # corrisponde a 100% di umidità
    max_val = 808  # corrisponde a 0% di umidità
    percentage = 100 - ((int(x) - min_val) * 100) / (max_val - min_val)

    # faccio si che il valore percentuale sia compreso tra 0 e 100 e lo porto ad una sola cifra decimale
    return round(max(0, min(percentage, 100)), 0)

while True:
    try:
        arduinoData = serialport.readline().decode('ascii')
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
