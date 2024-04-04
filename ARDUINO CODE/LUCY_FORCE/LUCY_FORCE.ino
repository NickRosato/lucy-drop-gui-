// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  delay(100);
  Serial.print("Time (s)");
  Serial.print(',');
  Serial.print("Voltage (V)");
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);
  // print out the value you read:
  
  float t = ((float) millis())/1000.0;
  Serial.print(t,3);
  Serial.print(',');
  Serial.println(voltage,3);
}
