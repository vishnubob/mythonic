/*
 CapacitiveSense.h v.04 - Capacitive Sensing Library for 'duino / Wiring
 Copyright (c) 2009 Paul Bagder  All right reserved.
 Version 04 by Paul Stoffregen - Arduino 1.0 compatibility, issue 146 fix
 Copyright (c) 2012 Giles Hall - Interrupt based method.
 vim: set ts=4:
 */

#if ARDUINO >= 100
#include "Arduino.h"
#else
//#include "WProgram.h"
#include "pins_arduino.h"
#include "WConstants.h"
#endif

#include "CapSense.h"

// Constructor /////////////////////////////////////////////////////////////////
// Function that handles the creation and setup of instances

CapSense::CapSense() {}

CapSense::CapSense(uint8_t sendPin, uint8_t receivePin)
{
	uint8_t sPort, rPort;

	// initialize this instance's variables
    current_value = 0;
    sensor_mode = SENSOR_CHARGE;
	MaxTotal = 1024;
    
	// get pin mapping and port for send Pin - from PinMode function in core
	sBit =  digitalPinToBitMask(sendPin);			// get send pin's ports and bitmask
	sPort = digitalPinToPort(sendPin);
	sReg = portModeRegister(sPort);
	sOut = portOutputRegister(sPort);				// get pointer to output register   

	rBit = digitalPinToBitMask(receivePin);			// get receive pin's ports and bitmask 
	rPort = digitalPinToPort(receivePin);
	rReg = portModeRegister(rPort);
	rIn  = portInputRegister(rPort);
   	rOut = portOutputRegister(rPort);
	
	// get pin mapping and port for receive Pin - from digital pin functions in Wiring.c
    noInterrupts();
	*sReg |= sBit;              // set sendpin to OUTPUT 
    interrupts();
}


bool CapSense::step_sensor(void)
{
    switch(sensor_mode)
    {
        case SENSOR_CHARGE:
            *sOut &= ~sBit;        // set Send Pin Register low
            
            *rReg &= ~rBit;        // set receivePin to input
            *rOut &= ~rBit;        // set receivePin Register low to make sure pullups are off
            
            *rReg |= rBit;         // set pin to OUTPUT - pin is now LOW AND OUTPUT
            *rReg &= ~rBit;        // set pin to INPUT 

            *sOut |= sBit;         // set send Pin High
            total = 0;
            sensor_mode = SENSOR_CHARGE_STEP;
            break;
        case SENSOR_CHARGE_STEP:
            // while receive pin is LOW AND total is positive value
            if ( !(*rIn & rBit) && (total < MaxTotal) ) 
            {
                total++;
            } else 
            {
                sensor_mode = SENSOR_DISCHARGE;
            }
            break;
        case SENSOR_DISCHARGE:
            // set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
            *rOut  |= rBit;        // set receive pin HIGH - turns on pullup 
            *rReg |= rBit;         // set pin to OUTPUT - pin is now HIGH AND OUTPUT
            *rReg &= ~rBit;        // set pin to INPUT 
            *rOut  &= ~rBit;       // turn off pullup

            *sOut &= ~sBit;        // set send Pin LOW
            sensor_mode = SENSOR_DISCHARGE_STEP;
            break;
        case SENSOR_DISCHARGE_STEP:
            // while receive pin is HIGH  AND total is less than timeout
            if ( (*rIn & rBit) && (total < MaxTotal) ) 
            {
                total++;
            } else
            {
                current_value = (total < MaxTotal) ? total : 0;
                sensor_mode = SENSOR_CHARGE;
                return true;
            }
            break;
    }
    return false;
}
