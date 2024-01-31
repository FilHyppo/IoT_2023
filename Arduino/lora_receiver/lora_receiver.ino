//arduino nero receiver

// valori sul 500 indicano terreno  bagnato (acqua = 412), sul 700 indicano terreno secco (aria = 800) e per valori più alti indicano terreno via via più secco
#include <SPI.h>
#include <LoRa.h>



unsigned long previousMillis = 0;  // Utilizzata per memorizzare il tempo del ciclo precedente
const long interval = 2000;        // Intervallo di tempo tra un ciclo e l'altro, cambiando questo valore regolo il delay


void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  while (!Serial);

  Serial.println("LoRa Receiver");

  if (!LoRa.begin(868E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {

  int umidita;
  unsigned int id;

  int packetSize = LoRa.parsePacket();
    // 1: read the input
    
  if (packetSize) {
    // received a packet
    Serial.print("Received packet ");

    // read packet
    while (LoRa.available()) {
      id = LoRa.parseInt();
      umidita = LoRa.parseInt();
      //stampa valori letti
      Serial.print("id: ");
      Serial.println(id);
      Serial.print(" umidita: ");
      Serial.println(umidita);
      
    }
    // 2: find the future state

    // 3: do the transition (i.e., change the state)

    // 4: update the output

    // 5: comunicazione seriale con bridge

    String messaggio = String(id) + " " + String(umidita);
    Serial.println(messaggio);  
  }
}