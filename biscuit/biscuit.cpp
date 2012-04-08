#include "arduino/Arduino.h"

#define GRN PD4
#define RED PD2

// Output
int redPin   = 6;   // Red LED,   connected to digital pin 9
int greenPin = 5;  // Green LED, connected to digital pin 10
int bluePin  = 3;  // Blue LED,  connected to digital pin 11
int redPin2   = 9;   // Red LED,   connected to digital pin 9
int greenPin2 = 10;  // Green LED, connected to digital pin 10
int bluePin2  = 11;  // Blue LED,  connected to digital pin 11

// Program variables
int redVal   = 255; // Variables to store the values to send to the pins
int greenVal = 1;   // Initial values are Red full, Green and Blue off
int blueVal  = 1;
int redVal2   = 255; // Variables to store the values to send to the pins
int greenVal2 = 1;   // Initial values are Red full, Green and Blue off
int blueVal2  = 1;

int i = 0;     // Loop counter    
int wait = 50; // 50ms (.05 second) delay; shorten for faster fades
int DEBUG = 0; // DEBUG counter; if set to 1, will write values back via serial

void setup()
{
  pinMode(redPin,   OUTPUT);   // sets the pins as output
  pinMode(greenPin, OUTPUT);   
  pinMode(bluePin,  OUTPUT); 
  pinMode(redPin2,   OUTPUT);   // sets the pins as output
  pinMode(greenPin2, OUTPUT);   
  pinMode(bluePin2,  OUTPUT); 

  pinMode(RED, OUTPUT);
  pinMode(GRN, OUTPUT);
  if (DEBUG) {           // If we want to see the pin values for debugging...
    Serial.begin(9600);  // ...set up the serial ouput on 0004 style
  }
  i = 0;
  redVal = 0xff;
  greenVal = 0;
  blueVal = 0;
  redVal2 = 0xff;
  greenVal2 = 0;
  blueVal2 = 0;
}

// Main program
void loop()
{
  analogWrite(redPin,   redVal);   // Write current values to LED pins
  analogWrite(greenPin, greenVal); 
  analogWrite(bluePin,  blueVal);  
  analogWrite(redPin2,   redVal);   // Write current values to LED pins
  analogWrite(greenPin2, greenVal); 
  analogWrite(bluePin2,  blueVal);  

  switch (i)
  {
    case 0:
        digitalWrite(RED, HIGH);
        redVal   -= 1; // Red down
        greenVal += 1; // Green up
        blueVal   = 0; // Blue low
        if (redVal == 0)
            i = 1;
        break;
    case 1:
        digitalWrite(GRN, HIGH);
        redVal    = 0; // Red low
        greenVal -= 1; // Green down
        blueVal  += 1; // Blue up
        if (greenVal == 0)
            i = 2;
        break;
    case 2:
        digitalWrite(RED, LOW);
        redVal  += 1; // Red up
        greenVal = 0; // Green low
        blueVal -= 1; // Blue down
        if (blueVal == 0)
            i = 0;
        break;
  }  

  delay(wait); // Pause for 'wait' milliseconds before resuming the loop
}


