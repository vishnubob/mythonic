/*
 CapacitiveSense.h v.04 - Capacitive Sensing Library for 'duino / Wiring
 Copyright (c) 2009 Paul Bagder  All right reserved.
 Version 04 by Paul Stoffregen - Arduino 1.0 compatibility, issue 146 fix
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
    current_value = 1;
	error = 1;
	
	CS_Timeout_Millis = 2000;
	CS_AutocaL_Millis = 20000;
    
	// get pin mapping and port for send Pin - from PinMode function in core
#ifdef NUM_DIGITAL_PINS
	if (sendPin >= NUM_DIGITAL_PINS) error = -1;
	if (receivePin >= NUM_DIGITAL_PINS) error = -1;
#endif
	
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
	leastTotal = 0x0FFFFFFFL;   // input large value for autocalibrate begin
	lastCal = millis();         // set millis for start
}

// Public Methods //////////////////////////////////////////////////////////////
// Functions available in Wiring sketches, this library, and other libraries

void CapSense::reset_CS_AutoCal(void)
{
	leastTotal = 0x0FFFFFFFL;
}

void CapSense::set_CS_AutocaL_Millis(unsigned long autoCal_millis)
{
	CS_AutocaL_Millis = autoCal_millis;
}

void CapSense::set_CS_Timeout_Millis(unsigned long timeout_millis)
{
	CS_Timeout_Millis = (timeout_millis * (float)loopTimingFactor * (float)F_CPU) / 16000000;  // floats to deal with large numbers
}

// Functions only available to other functions in this library

void CapSense::step_sensor(void)
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
            sensor_mode = SENSOR_CHARGE_STEP;
            break;
        case SENSOR_CHARGE_STEP:
            // while receive pin is LOW AND total is positive value
            if ( !(*rIn & rBit) && (total < CS_Timeout_Millis) ) 
            {
                total++;
                break;
            }
            sensor_mode = SENSOR_DISCHARGE;
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
            if ( (*rIn & rBit) && (total < CS_Timeout_Millis) ) 
            {
                total++;
                break;
            }
            sensor_mode = SENSOR_CALIBRATE;
            break;
        case SENSOR_CALIBRATE:
            sensor_mode = SENSOR_CHARGE;
            // only calibrate if time is greater than CS_AutocaL_Millis and total is less than 10% of baseline
            // this is an attempt to keep from calibrating when the sensor is seeing a "touched" signal
            if ((millis() - lastCal > CS_AutocaL_Millis) && abs(total - leastTotal) < (int)(.10 * (float)leastTotal)) 
            {
                // reset for "autocalibrate"
                leastTotal = 0x0FFFFFFFL;          
                lastCal = millis();
            }
            if (total < leastTotal)
            {
                total = leastTotal;
            }
            total = total - leastTotal;
            current_value = total;
            break;
    }
}
