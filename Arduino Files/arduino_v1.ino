
#include <SPI.h>
#include <SD.h>

#define relay_port 6
#define thermistor 5
#define battery 2
#define sdPort 10
#define Rbat2 10000 // ohms
#define Rtherm2 100000 // ohms
char logFilename[] = "log.csv";

//serial monitor print while writing log
boolean serialPrint = true;//true or false 
boolean sdPrint = true;//true or false 

 
File myFile;
 
void setup() {
   Serial.begin(9600);
   pinMode(relay_port,OUTPUT);
   while (!Serial) {
     ; // wait for serial port to connect. Needed for native USB port only
   }
   if (sdPrint){ 
     Serial.print("Initializing SD card...");
   
     if (!SD.begin(sdPort)) {
       Serial.println("initialization failed!");
       while (1);
     }
     Serial.println("initialization done.");
      SD.remove(logFilename);
     // open the file. note that only one file can be open at a time,
     // so you have to close this one before opening another.
       myFile = SD.open(logFilename, FILE_WRITE);
   
      if (!myFile) {
       Serial.println("log file missing");
       while(1);
      }
   }
}

void writeToLog(float voltage, float temp ) {
    if (sdPrint){ 
      myFile = SD.open(logFilename, FILE_WRITE);
      myFile.print(millis()/1000);
      myFile.print(", ");
      myFile.print(voltage);
      myFile.print(", ");  
      myFile.println(temp);  
      // close the file:
      myFile.close();
    }

    if(serialPrint){
//       Serial.print ("Time:");
//       Serial.print(millis()/1000);  
//       Serial.print ("  Voltage: ");
//       Serial.print(voltage);
         Serial.print(millis()/1000);
         Serial.print(", ");
         Serial.print(voltage);
         Serial.print(", ");  
         Serial.println(temp);
    } 
}
 
void loop() {
  // voltage divider
  float Vtherm = analogRead(thermistor);
  float Vopencircuit = analogRead(battery)* 5.0 / 1023.0;
//  float perc_charge = Vbat/1.09;
  float Rtherm = Rtherm2 * (1023.0 / (float)Vtherm - 1.0);
  float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
  float Temp = (1.0 / (c1 + c2*log(Rtherm) + c3*log(Rtherm)*log(Rtherm)*log(Rtherm))) - 273.15;
  

//  if(Temp > 20) {
//    digitalWrite(relay_port, HIGH);
//    Serial.print("HIGH----------------HIGH----------------HIGH----------------");
//  } else {
//    digitalWrite(relay_port,LOW);
//  }

  delay(900);

  writeToLog(Vopencircuit*(100+10)/10, Temp);
 }
