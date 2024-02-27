//File - testing 2 - adding dht and nodemcu to testing file

//testing file desc: GPS, GSM, Switch, Smoke sensor working - Tarun S 08-12-2023

//testing2 file desc: integrating diff func for reading sensor values

#define USE_ARDUINO_INTERRUPTS true   
#include <PulseSensorPlayground.h> 

#include "DHT.h"
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

#define GSM_RX_PIN 8 // exchange tx rx while doing connection for gps
#define GSM_TX_PIN 9

#define GPS_RX_PIN 6
#define GPS_TX_PIN 7

#define SWITCH_PIN 2  

#define DHTPIN 3
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const int vibrationPin = A2;
const int PulseWire = 4; 
int smokesensor = A0;
int Threshold = 550;

PulseSensorPlayground pulseSensor;


SoftwareSerial sim800l(GSM_RX_PIN, GSM_TX_PIN);
SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);
TinyGPSPlus gps;

//9148599609
const char* phoneNumber = "+917337756029";  // Replace with your phone number
int analog = analogRead(smokesensor);


void setup() {

  Serial.begin(9600);
  sim800l.begin(9600);
  gpsSerial.begin(9600);

  pinMode(SWITCH_PIN, INPUT_PULLUP);

  dht.begin();

  pulseSensor.analogInput(PulseWire);   
  pulseSensor.setThreshold(Threshold);  
  if (pulseSensor.begin()) {
    Serial.println("Pulse active");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
}


void loop() {

  gpsLoop(); //This is to start gps

  //Temperature sensor
  float t = dht.readTemperature();

//   if (pulseSensor.sawStartOfBeat()) {           
//   int myBPM = pulseSensor.getBeatsPerMinute();                                               
//     Serial.print("BPM: ");                       
//     Serial.println(myBPM);                      
// }
  
  if (digitalRead(SWITCH_PIN) == HIGH) {
    Serial.println("SWITCH ON");
    sendHelpMessage();
    delay(5000); 
  }
  else if(digitalRead(SWITCH_PIN) == LOW){
    sendDataToCsv();
    checkingValueFunction();
  }

  else if(analog>900){
    Serial.println(analog);
    Serial.println("Fire detected!");
    sendHelpMessage();
  }

}

void gpsLoop() {
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isValid()) {
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();

    String googleMapsLink = "http://maps.google.com/maps?q=" + String(latitude, 6) + "," + String(longitude, 6);

    Serial.println(googleMapsLink);
    delay(5000);
  }
}

void sendHelpMessage() {
  float latitude = gps.location.lat();
  float longitude = gps.location.lng();

  String message = "Help! I am in DANGER!, here is my location:  ";
  message += gps.location.lat();
  message += ",";
  message += gps.location.lng();
  message += " http://maps.google.com/maps?q=";
  message += String(latitude, 6);
  message += ",";
  message += String(longitude, 6);

  sendMessage(phoneNumber, message);
  Serial.println("HELP Message sent.");
}

void sendMessage(const char* number, String message) {
  sim800l.println("AT+CMGF=1"); 
  delay(1000);
  sim800l.print("AT+CMGS=\"");
  sim800l.print(number);
  sim800l.println("\"");
  delay(1000);
  sim800l.println(message);
  delay(1000);
  sim800l.write(26); 
  delay(1000);
}

void sendDataToCsv() {
  float t = dht.readTemperature();
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println("°C");
  delay(2000);
}

// void sendTemperatureToGoogleSheet(float t){
//   espSerial.println("AT+CIPSTART=\"TCP\",\"script.google.com\",80");
//   if(espSerial.find("OK")){
//     String data = "GET /macros/s/AKfycby1UxQHh5dqInIMAa4hufK7nhm2bKS30QPFQFn3WEp6BJ5vv3yo54Avi1pYuTguHGzw/exec?func=addData&val=" + String(t) + " HTTP/1.0\r\n\r\n";
//     espSerial.print("AT+CIPSEND=");
//     espSerial.println(data.length());
//     if (espSerial.find(">")) {
//       espSerial.print(data);
//     }
//   }
//   espSerial.println("AT+CIPCLOSE");
// }

void checkingValueFunction(){

  int smokeSensorValue = analogRead(A0);
  int vibrationValue = analogRead(vibrationPin);
  int myBPM = pulseSensor.getBeatsPerMinute();

  Serial.print("Pulse: ");                        
  Serial.println(myBPM);                       

  Serial.print("Smoke: ");
  Serial.println(smokeSensorValue);

  Serial.print("Vibration: ");
  Serial.println(vibrationValue);

  delay(1000);

  if(smokeSensorValue > 200 && myBPM>200){
    Serial.println("FIRE DETECTED!");
    sendHelpMessage();
  }
  else if(vibrationValue > 999 && myBPM>200){
    Serial.println("HIGH VIBRATION DETECTED!");
    sendHelpMessage();
  }
  // else if(myBPM>200){
  //   Serial.println("HIGH PULSE DETECTED!");
  //   sendHelpMessage();
  // }
}
  
