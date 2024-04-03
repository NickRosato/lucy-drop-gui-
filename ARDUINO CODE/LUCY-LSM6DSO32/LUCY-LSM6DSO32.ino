// Basic demo for accelerometer & gyro readings from Adafruit
// LSM6DSO32 sensor

#include <Adafruit_LSM6DSO32.h>

// For SPI mode, we need a CS pin
#define LSM_CS 10
// For software-SPI mode we need SCK/MOSI/MISO pins
#define LSM_SCK 13
#define LSM_MISO 12
#define LSM_MOSI 11

Adafruit_LSM6DSO32 dso32;
void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  if (!dso32.begin_I2C()) {
    // if (!dso32.begin_SPI(LSM_CS)) {
    // if (!dso32.begin_SPI(LSM_CS, LSM_SCK, LSM_MISO, LSM_MOSI)) {
    // Serial.println("Failed to find LSM6DSO32 chip");
    while (1) {
      delay(10);
    }
  }

  dso32.setAccelRange(LSM6DSO32_ACCEL_RANGE_32_G);
  dso32.setAccelDataRate(LSM6DS_RATE_208_HZ);

  Serial.print("Time (s)");
  Serial.print(',');
  Serial.print("X (m/s^2)");
  Serial.print(',');
  Serial.print("Y (m/s^2)");
  Serial.print(',');
  Serial.println("Z (m/s^2)");
}

void loop() {

  //  /* Get a new normalized sensor event */
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  dso32.getEvent(&accel, &gyro, &temp);
  float x = accel.acceleration.x;
  float y = accel.acceleration.y;
  float z = accel.acceleration.z;
  float t = ((float) millis())/1000.0;

  Serial.print(t,3);
  Serial.print(',');
  Serial.print(x,3);
  Serial.print(',');
  Serial.print(y,3);
  Serial.print(',');
  Serial.println(z,3);
  
}