#include <LoRa.h>
#include <SoilMoisture.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <RTClib.h>  //rtc serve per prendere l'ora ttuale, è un modulino da comprare

RTC_DS3231 rtc;

const int soilMoisturePin = A0;  // Pin analogico a cui è collegato il sensore

const int csPin = 10;  // Pin CS del modulo LoRa
const int resetPin = 9;  // Pin di reset del modulo LoRa
const int irqPin = 2;  // Pin IRQ del modulo LoRa (può variare)


void setup() {
  Serial.begin(9600);
  while (!Serial);  //Questa riga aspetta che la comunicazione seriale sia disponibile prima di continuare l'esecuzione del programma. 
  //In pratica, aspetta finché il tuo computer non stabilisce una connessione con il microcontrollore attraverso la porta seriale USB.

  if (!LoRa.begin(433E6)) { /*Inizializza il modulo LoRa con una frequenza di 433 MHz (specificata da 433E6). 
  Se l'inizializzazione del modulo LoRa non è riuscita, viene eseguito while (1) che entra in un loop infinito, bloccando il programma*/
    Serial.println("Errore inizializzazione modulo LoRa");
    while (1);
  }
    Serial.println("Modulo LoRa inizializzato correttamente");

  if (!rtc.begin()) {
    Serial.println("Impossibile trovare il modulo RTC");
    while (1);
  }

  if (rtc.lostPower()) {
    Serial.println("Il modulo RTC ha perso l'alimentazione, reimpostazione dell'orologio!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

}

void loop() {
  delay(2000);

  int soilMoistureValue = leggiValoreUmiditaSuolo();

  Serial.print("Umidità del suolo: ");
  Serial.println(soilMoistureValue);

  inviaDatiAlServer(soilMoistureValue);
}

int leggiValoreUmiditaSuolo() {
  int value = analogRead(soilMoisturePin);

  return value;
}



void inviaDatiAlServer(int valoreUmiditaSuolo) {
  String dataCorrente = getTime(); 

  // Crea un oggetto JSON
  DynamicJsonDocument jsonDocument(128);  // 128 è la dimensione del JSON, l'ho messo piccolo senza saper nè leggere nè scrivere perchè arduino ha poca memoria
  jsonDocument["data"] = dataCorrente;
  jsonDocument["umidita"] = valoreUmiditaSuolo;

  // conversione dell'oggetto JSON in una stringa
  String jsonString;
  serializeJson(jsonDocument, jsonString);

  // Invia i dati attraverso LoRa
  LoRa.beginPacket();
  LoRa.print(jsonString);
  LoRa.endPacket();

  Serial.println("Dati inviati al server (JSON): " + jsonString);
}

String getTime() {
  DateTime now = rtc.now();
  String formattedTime = String(now.year()) + "-" + padZero(now.month()) + "-" + padZero(now.day()) + " " +
                         padZero(now.hour()) + ":" + padZero(now.minute()) + ":" + padZero(now.second());
  return formattedTime;
}

String padZero(int value) {
  if (value < 10) {
    return "0" + String(value);
  } else {
    return String(value);
  }
}

