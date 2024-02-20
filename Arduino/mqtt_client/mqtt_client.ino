#include <ArduinoMqttClient.h>
#include "WiFiS3.h"
#include "secrets.h"
#include "Arduino_LED_Matrix.h"
ArduinoLEDMatrix matrix;

byte frame[8][12] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};


char ssid[] = MY_WIFI_SSID;  // network SSID
char pass[] = MY_WIFI_PASS;  // network password

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "172.20.10.2";
int port = 1883;
const char topic[] = "/irrigatore/abcdef";
int durata = 0;


void setup() {
  Serial.begin(9600);
  matrix.begin();
  pinMode(11, OUTPUT);

  while (!Serial) {
    ;
  }
  // connessione alla rete wifi:
  Serial.print("provo a connettermi a: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // attesa connessione
    //Serial.print(".");
    //delay(5000);
  }

  Serial.println("connesso");
  Serial.println();

  Serial.print("provo a connettermi al broker MQTT: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("connessione fallita! errore = ");
    Serial.println(mqttClient.connectError());

    while (1)
      ;
  }

  Serial.println("connesso al broker MQTT!");
  Serial.println();

  // setto la callback, ovvero quello che faccio quando ricevo un messaggio
  mqttClient.onMessage(onMqttMessage);

  Serial.print("Mi iscrivo al topic: ");
  Serial.println(topic);
  Serial.println();

  // iscrizione al topic
  mqttClient.subscribe(topic, 2);


  // posso disiscrivermi:
  // mqttClient.unsubscribe(topic);

  Serial.print("Topic: ");
  Serial.println(topic);

  Serial.println();
}

void loop() {
  // chiamo poll() regolarmente per poter ricevere i messaggi MQTT e
  // mandare MQTT keep alive che evitano di farmi disconnettere dal broker
  mqttClient.poll();
}

void onMqttMessage(int messageSize) {
  // messaggio ricevuto, stampo le informazioni
  Serial.print("Ricevuto un messaggio del topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', di lunghezza ");
  Serial.print(messageSize);
  Serial.println(" bytes:");

  // leggo il contenuto del messaggio e lo elaboro
  String messaggio = "";  // Stringa per memorizzare il messaggio letto

  while (mqttClient.available()) {
    char carattere = mqttClient.read();
    if (isdigit(carattere)) {
      messaggio += carattere;
    }
  }
  durata = messaggio.toInt();
  Serial.print("la durata dell'irrigazione è di ");
  Serial.print(durata);
  Serial.println(" secondi");

  //conto alla rovescia sulla matrice di led
  digitalWrite(11, LOW);

  unsigned long t = millis();

  for (int i = durata; i >= 0; i--) {
    clearDisplay();

    int u = i % 10;
    int d = (i / 10) % 10;
    int c = (i / 100) % 10;

    digit(u, 8, 0);
    digit(d, 4, 0);
    digit(c, 0, 0);

    matrix.renderBitmap(frame, 8, 12);

    while (millis() - t < 1000) {
    }

    t = millis();
  }
  digitalWrite(11, HIGH);
  t = millis();
  while (millis() - t < 500) {
  }
  digitalWrite(11, LOW);
}



void clearDisplay() {
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 12; j++) {
      frame[i][j] = 0;
    }
  }
}

void digit(int n, int offx, int offy) {
  switch (n) {
    case 0:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 0;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 1;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 1:
      frame[offy][offx + 0] = 0;
      frame[offy][offx + 1] = 0;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 0;
      frame[offy + 1][offx + 1] = 1;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 0;
      frame[offy + 2][offx + 1] = 0;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 0;
      frame[offy + 4][offx + 1] = 0;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 2:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 0;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 1;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 0;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 3:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 0;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 4:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 0;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 0;
      frame[offy + 4][offx + 1] = 0;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 5:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 0;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 6:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 0;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 1;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 7:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 0;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 0;
      frame[offy + 2][offx + 1] = 0;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 0;
      frame[offy + 4][offx + 1] = 0;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 8:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 1;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
    case 9:
      frame[offy][offx + 0] = 1;
      frame[offy][offx + 1] = 1;
      frame[offy][offx + 2] = 1;

      frame[offy + 1][offx + 0] = 1;
      frame[offy + 1][offx + 1] = 0;
      frame[offy + 1][offx + 2] = 1;

      frame[offy + 2][offx + 0] = 1;
      frame[offy + 2][offx + 1] = 1;
      frame[offy + 2][offx + 2] = 1;

      frame[offy + 3][offx + 0] = 0;
      frame[offy + 3][offx + 1] = 0;
      frame[offy + 3][offx + 2] = 1;

      frame[offy + 4][offx + 0] = 1;
      frame[offy + 4][offx + 1] = 1;
      frame[offy + 4][offx + 2] = 1;
      break;
  }
}
