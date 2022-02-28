#include <SPI.h>
#include <LoRa.h>

String r = "";
int packetSize;
char sread;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSyncWord("0x01");
  Serial.print("READY. Waiting for serial. ");
}

void loop() {
  
  while(Serial.available())
  {            
    sread = Serial.read();   
    if(sread != '*')
    {
      r.concat(sread);
    }
    
   
  }
  if(r != "" & sread == '*')
  {
    LoRa.beginPacket();
    LoRa.print(r);
    LoRa.endPacket();
    r = "";
    Serial.print(r);
  }
  packetSize = LoRa.parsePacket();
  if (packetSize) {
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
  }

}
