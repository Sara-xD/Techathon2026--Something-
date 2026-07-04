// Office Watch — one-room ESP32 node (representative circuit)
// -----------------------------------------------------------------------------
// Reads the ON/OFF state of 2 fans + 4 lights, mirrors each on an LED, and reads
// the room's aggregate current, then prints a JSON line (what a real node would
// POST to the backend over Wi-Fi).
//
// In a real build the sense inputs come from AC optocouplers and the current
// reading from an ACS712/CT clamp. In the Wokwi simulation:
//   - each sense input  <- a slide switch (switch = that device is energised)
//   - the current input <- a potentiometer (turn it = more room current)
//   - each mirror LED shows what is ON at a glance
//
// Pin map matches diagrams/circuit-guide.md and circuit-wiring-diagram.svg.
//
// NOTE: this is an Arduino sketch (C++). The file must end in .ino or .cpp --
// NOT .c. In a .ino file the include below is automatic; it's kept here so the
// sketch also works if you save it as main.cpp.
// -----------------------------------------------------------------------------
#include <Arduino.h>

const int   SENSE_PINS[6] = {13, 14, 23, 22, 18, 19};   // Fan1, Fan2, Light1..4
const int   LED_PINS[6]   = {12, 27, 26, 25, 33, 32};   // mirror LEDs
const char* LABELS[6]     = {"Fan 1", "Fan 2", "Light 1", "Light 2", "Light 3", "Light 4"};
const int   RATED_W[6]    = {60, 60, 15, 15, 15, 15};   // rated watts per device
const int   CURRENT_PIN   = 34;                         // ADC1 (ADC2 clashes with Wi-Fi)
const int   ROOM_MAX_W    = 2 * 60 + 4 * 15;            // one room all-on = 180 W (current sensor full-scale)

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 6; i++) {
    pinMode(SENSE_PINS[i], INPUT_PULLDOWN);  // defined LOW when a device is off
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop() {
  int    estWatts = 0;
  String devices  = "";

  for (int i = 0; i < 6; i++) {
    bool on = digitalRead(SENSE_PINS[i]) == HIGH;
    digitalWrite(LED_PINS[i], on ? HIGH : LOW);        // mirror state on the board
    if (on) estWatts += RATED_W[i];
    devices += String("\"") + LABELS[i] + "\":" + (on ? "true" : "false");
    if (i < 5) devices += ",";
  }

  // ACS712 / potentiometer -> 0..4095 -> plausible 0..180 W room current.
  int raw          = analogRead(CURRENT_PIN);
  int sensedWatts  = map(raw, 0, 4095, 0, ROOM_MAX_W);

  // One JSON line = the payload a real node would POST to the backend /ingest
  // endpoint. (In this project the backend simulator produces this same shape.)
  Serial.print("{\"room\":\"work1\",\"devices\":{");
  Serial.print(devices);
  Serial.print("},\"estWatts\":");
  Serial.print(estWatts);
  Serial.print(",\"sensedWatts\":");
  Serial.print(sensedWatts);
  Serial.println("}");

  delay(1000);
}
