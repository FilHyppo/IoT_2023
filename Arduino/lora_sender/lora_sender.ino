//arduino verde sender
// valori sul 500 indicano terreno  bagnato (acqua = 412), sul 700 indicano terreno secco (aria = 808) e per valori più alti indicano terreno via via più secco

#include <SPI.h>
#include <LoRa.h>
#define reset 9
#define ss 10

const unsigned int id = 4000;
int count = 0;
unsigned long previousMillis = 0;  // Utilizzata per memorizzare il tempo del ciclo precedente
const long interval = 2000;        // Intervallo di tempo tra un ciclo e l'altro, cambiando questo valore regolo il delay


void setup() {
  Serial.begin(9600);
  LoRa.setPins(ss, reset);
  pinMode(13, OUTPUT);
  while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  unsigned long currentMillis = millis();  // Memorizza il tempo corrente
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Memorizza il tempo corrente
    // 1: read the input
    int umidita;
    umidita = analogRead(A0);
    
    // 2: find the future state

    // 3: do the transition (i.e., change the state)

    // 4: update the output

    count++;

    //stampe varie
    Serial.print("Sending packet: ");
    Serial.println(count);
    Serial.print(" umidita: ");
    Serial.println(umidita);
    Serial.print(" id: ");
    Serial.println(id);
    

    //send packet 
    LoRa.beginPacket();
    LoRa.print(id);
    LoRa.print(".");  //serve per il parse int del receiver perchè legge tutti i byte che sono numeri quindi col . spezzo i valori
    LoRa.print(umidita);
    LoRa.endPacket();
  }
}