// Include the Wire library for I2C
#include <Wire.h>
#include <Servo.h>
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
const int pumpe1 = 5;
const int pumpe2 = 6;
//vekstlys
const int vekstlys = 4;
int toggle = false;
//int pos = 0;    // variable to store the servo position

const unsigned long delayTime = 2000;  // delay time in milliseconds
const int max = 255;
char c;

//Flowmåler
byte statusLed    = 13;
byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorInterrupt2 = 1;  // 0 = digital pin 3
byte sensorPin       = 2;
byte sensorPin2       = 3;
// The hall-effect flow sensor outputs approximately 98 pulses per second per
// litre/minute of flow.
float calibrationFactor = 98/2;
float calibrationFactor2 = 98/2;
volatile byte pulseCount;  
volatile byte pulseCount2; 
float flowRate;
float flowRate2;
unsigned int flowMilliLitres;
unsigned int flowMilliLitres2;
unsigned long totalMilliLitres;
unsigned long totalMilliLitres2;
unsigned long oldTime;
unsigned long oldTime2;
int pump1;
int pump2;


int pos = 120; // starting position
int increment = 0; // default increment


void setup() {
//Øvrige
  Serial.begin(9600);
  Wire.begin(0x38);
  pinMode(pumpe1, OUTPUT);
  pinMode(pumpe2, OUTPUT);
  pinMode(vekstlys, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(pos);
  // activate internal pullups for twi.
  digitalWrite(SDA, 1);
  digitalWrite(SCL, 1);  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);

//Flowmåler
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  pinMode(sensorPin, INPUT);
  pinMode(sensorPin2, INPUT);
  digitalWrite(sensorPin, HIGH);
  digitalWrite(sensorPin2, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  pulseCount2        = 0;
  flowRate2          = 0.0;
  flowMilliLitres2   = 0;
  totalMilliLitres2  = 0;
  oldTime2           = 0;
  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING); 
  
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    c = Wire.read(); // receive byte as a character
    loop();
   }
  
}



void loop() {

if(c==1){totalMilliLitres = 0;pump1=1;}
if(c==2){totalMilliLitres = 0;pump2=1;}

//-----------------------------Pumpe1-----------------------------------------------
if (totalMilliLitres > 20 && pump1 == 1) {
    analogWrite(pumpe1, 0); // turn off pump if totalMilliLitres is greater than 10
    pump1 = 0;
  } else if (pump1 == 1) {
     analogWrite(pumpe1, 200);
     
  }

  
//-----------------------------Pumpe2-----------------------------------------------
  
if (totalMilliLitres > 20 && pump2 == 1) {
    analogWrite(pumpe2, 0); // turn off pump if totalMilliLitres is greater than 10
    pump2 = 0;
  } else if (pump2 == 1) {
     analogWrite(pumpe2, 200);
  }



  if(c==3){
    digitalWrite(pumpe1, 0);
    digitalWrite(pumpe2, 0);
  }


//-----------------------------Vekstlys----------------------------------------------

  if(c==4){
    digitalWrite(vekstlys, true);
  }

   if(c==5){
    digitalWrite(vekstlys, false);
  }

//----------------------------Servo---------------------------------------------------

if (c == 6) {
  delay(200);
  increment = 3;
  if (pos > 90) { // check if pos is above the lower limit
    pos -= increment;
  }
  myservo.write(pos);
}
if (c == 7) {
  delay(200);
  increment = 3;
  if (pos < 150) { // check if pos is below the upper limit
    pos += increment;
  }
  myservo.write(pos);
}

//Flowmåler
//----------------------------Pumpe1---------------------------------------------

if((millis() - oldTime) > 1000)    // Only process counters once per second
  { 
    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt);
    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    oldTime = millis();
    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres = (flowRate / 60) * 1000;
    // Add the millilitres passed in this second to the cumulative total
    totalMilliLitres += flowMilliLitres; 
    unsigned int frac;

    // Print the cumulative total of litres flowed since starting
    Serial.print("Output Liquid Quantity: ");        
    Serial.print(totalMilliLitres);
    Serial.println("mL"); 
    Serial.print("\t"); 		  // Print tab space

    // Reset the pulse counter so we can start incrementing again
    pulseCount = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }


//----------------------------Pumpe2---------------------------------------------


if((millis() - oldTime2) > 1000)    // Only process counters once per second
  { 
    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt2);
    flowRate2 = ((1000.0 / (millis() - oldTime2)) * pulseCount) / calibrationFactor2;
    oldTime2 = millis();
    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres2 = (flowRate2 / 60) * 1000;
    // Add the millilitres passed in this second to the cumulative total
    totalMilliLitres2 += flowMilliLitres2; 
    unsigned int frac2;

    // Print the cumulative total of litres flowed since starting
    Serial.print("Output Liquid Quantity2: ");        
    Serial.print(totalMilliLitres2);
    Serial.println("mL"); 
    Serial.print("\t"); 		  // Print tab space


    // Reset the pulse counter so we can start incrementing again
    pulseCount2 = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt2, pulseCounter, FALLING);
  }

}


//Insterrupt Service Routine

void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
