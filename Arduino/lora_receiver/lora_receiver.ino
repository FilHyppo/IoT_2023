//arduino nero receiver

// valori sul 500 indicano terreno  bagnato (acqua = 412), sul 700 indicano terreno secco (aria = 808) e per valori più alti indicano terreno via via più secco
#include <SPI.h>
#include <LoRa.h>
#define reset 9
#define ss 10

void setup() {
  Serial.begin(9600);
  LoRa.setPins(ss, reset);
  pinMode(13, OUTPUT);
  while (!Serial);

  //Serial.println("LoRa Receiver");

  if (!LoRa.begin(433E6)) {
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
    //Serial.print("Received packet ");

    // read packet
    while (LoRa.available()) {
      id = LoRa.parseInt();
      umidita = LoRa.parseInt();
      //stampa valori letti
      Serial.print("id: ");
      Serial.print(id);
      Serial.print(" umidita: ");
      Serial.println(umidita);
      
    }
    // 2: find the future state

    // 3: do the transition (i.e., change the state)

    // 4: update the output

    // 5: comunicazione seriale con bridge

    //String messaggio = String(id) + " " + String(umidita);
    //Serial.println(messaggio);
  }
}