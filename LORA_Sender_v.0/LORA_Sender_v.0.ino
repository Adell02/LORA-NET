#include <SPI.h>
#include <LoRa.h>

String spl;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.print("READY. Waiting for serial. ");
}

void loop() {
  
  serialReceive();
}

void serialReceive()
{
  while(Serial.available())
  {
    String r = Serial.readString();
    /*
    if(r.length() > 255)
    {
      Serial.println("String too long. Splitting message.");
      int i =0;
      do
      {
        spl = r.substring(255*i,255+255*i);
        sending(spl);
        Serial.println(spl);
        i++;
      }while(spl.length() > 0);     
    }
    else{
    sending(r);
    Serial.println(r);
    }
  }*/
  sending(r);
}}

void sending(String m)
{
  LoRa.beginPacket();
  LoRa.print(m);
  LoRa.endPacket();
}
