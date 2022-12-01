#define relay_port 6
#define thermistor 5
#define battery 2
#define Rbat2 10000 // ohms
#define Rtherm2 100000 // ohms


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(relay_port,OUTPUT);
}

void loop() {
  // voltage divider
  float Vtherm = analogRead(thermistor);
  float Vbat = analogRead(battery)* 5.0 / 1023.0;
  float perc_charge = Vbat/1.09;
  float Rtherm = Rtherm2 * (1023.0 / (float)Vtherm - 1.0);
  float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
  float Temp = (1.0 / (c1 + c2*log(Rtherm) + c3*log(Rtherm)*log(Rtherm)*log(Rtherm))) -273.15;
  

  Serial.println("Voltage bat (V): "); 
  Serial.println(Vbat*11);
  Serial.println("Charge (%): "); 
  Serial.println(perc_charge);
  Serial.println("Thermistor reading: "); 
  Serial.println(Rtherm);
  Serial.println("Temp: "); 
  Serial.println(Temp);
  //digitalWrite(8,HIGH);
  

  if(Temp > 20) {
    digitalWrite(relay_port, HIGH);
    Serial.print("HIGH----------------HIGH----------------HIGH----------------");
  } else {
    digitalWrite(relay_port,LOW);
  }
  delay(500);
}
