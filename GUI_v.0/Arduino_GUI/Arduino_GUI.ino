#include <SPI.h>
#include <LoRa.h>

String r = "";
int packetSize;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSyncWord("0x01");
  LoRa.enableCrc();
  Serial.print("READY. Waiting for serial. ");
}

void loop() {
  
  while(Serial.available())
  {    
    r.concat((char)Serial.read());
  }
  if(r != "")
  {
    LoRa.beginPacket();
    LoRa.print(r);
    LoRa.endPacket();
    Serial.print(" ");
    r = "";
  }
  packetSize = LoRa.parsePacket();
  if (packetSize) {
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
  }

}
