#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL375.h>

#define ADXL375_SCK 13
#define ADXL375_MISO 12
#define ADXL375_MOSI 11
#define ADXL375_CS 10

/* Assign a unique ID to this sensor at the same time */
/* Uncomment following line for default Wire bus      */
Adafruit_ADXL375 accel = Adafruit_ADXL375(12345);

/* Uncomment for software SPI */
//Adafruit_ADXL375 accel = Adafruit_ADXL375(ADXL375_SCK, ADXL375_MISO, ADXL375_MOSI, ADXL375_CS, 12345);

/* Uncomment for hardware SPI */
//Adafruit_ADXL375 accel = Adafruit_ADXL375(ADXL375_CS, &SPI, 12345);

void setup(void)
{
  Serial.begin(115200);
  accel.begin();
  delay(100);
  
  /* Initialise the sensor */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL343 ... check your connections */
    Serial.println("Ooops, no ADXL375 detected ... Check your wiring!");
    while(1);
  }
  accel.setTrimOffsets(0, 0, 0);
  delay(10);

  float x = accel.getX();
  float y = accel.getY();
  float z = accel.getZ();

  accel.setTrimOffsets(-(x+2)/4, 
                       -(y+2)/4, 
                       -(z-20+2)/4);  // Z should be '20' at 1g (49mg per bit)
  // Range is fixed at +-200g

  Serial.print("Time (s)");
  Serial.print(',');
  Serial.print("X (m/s^2)");
  Serial.print(',');
  Serial.print("Y (m/s^2)");
  Serial.print(',');
  Serial.println("Z (m/s^2)");
  
}

void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  accel.getEvent(&event);

  float x = event.acceleration.x;
  float y = event.acceleration.y;
  float z = event.acceleration.z;
  float t = ((float) millis())/1000.0;

  Serial.print(t,3);
  Serial.print(',');
  Serial.print(x,3);
  Serial.print(',');
  Serial.print(y,3);
  Serial.print(',');
  Serial.println(z,3);
  

  
}