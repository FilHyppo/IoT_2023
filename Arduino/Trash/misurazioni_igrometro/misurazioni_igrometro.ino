// valori sul 500 indicano terreno  bagnato (acqua = 412), sul 700 indicano terreno secco (aria = 800) e per valori più alti indicano terreno via via più secco

int iCurrentState = 0;
// 0: S1 = spento, 1: S2 = acceso
int count = 0;
const unsigned int id = 1;
unsigned long previousMillis = 0;  // Utilizzata per memorizzare il tempo del ciclo precedente
const long interval = 2000;        // Intervallo di tempo tra un ciclo e l'altro, cambiando questo valore regolo il delay


void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();  // Memorizza il tempo corrente
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Memorizza il tempo corrente
    // 1: read the input
    int umidita;
    umidita = analogRead(A0);

    // 2: find the future state
    int iFutureState;
    iFutureState = iCurrentState;

    if (iCurrentState == 0 && umidita <= 600)
      iFutureState = 1;  // terreno bagnato
    if (iCurrentState == 0 && umidita >= 600)
      iFutureState = 0;  // terreno asciutto
    if (iCurrentState == 1 && umidita <= 600)
      iFutureState = 1;  // terreno bagnato
    if (iCurrentState == 1 && umidita >= 600)
      iFutureState = 0;  // terreno asciutto

    // 3: do the transition (i.e., change the state)
    iCurrentState = iFutureState;

    // 4: update the output
    if (iCurrentState == 0)
      digitalWrite(13, LOW);
    else
      digitalWrite(13, HIGH);
    count++;

    // 5: stampe varie
    String messaggio = String(id) + " " + String(umidita) + " " + String(count);
    Serial.println(messaggio);
  }
}