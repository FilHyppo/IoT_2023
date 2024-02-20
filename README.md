# IoT_2023
Progetto IoT UNIMORE

Istruzioni per esame:

Assicurarsi che il server redis sia in esecuzione.
    $ redis-cli ping (deve rispondere con PONG)
Assicurarsi che il broker MQTT sia in esecuzione.
    $ mosquitto_sub -t "test" (deve essere in grado di ricevere messaggi)
    $ mosquitto_pub -t "test" -m "hello world" (deve essere in grado di inviare messaggi)

MUOVERSI DENTRO LA CARTELLA IoTWebsiteREST e aprire l'ambiente virtuale: (per ogni terminale usato)
    $ pipenv shell

MUOVERSI DENTRO LA CARTELLA DEL PROGETTO (quella che contiene il file manage.py)
Lanciare il server django sul tuo indirizzo IP asseganto dalla rete dell'hotspot del tuo telefono.
    $ python3 manage.py runserver <ip_address>:8000

Lanciare worker e beat celery.
    $ celery -A djangoproject worker -l info (nel caso di errore aggiungere opzione "-P solo" e chiamatemi)
    $ celery -A djangoproject beat -l info
    [$ celery -A djangoproject flower -l info (in caso di necessità di debug)]

Eseguire ognuno in un terminale separato, assicurandosi di essere all'interno dell'ambiente virtuale