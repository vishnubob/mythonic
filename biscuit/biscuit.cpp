#include "arduino/Arduino.h"
#include "arduino/EEPROM.h"
#include "CapSense/CapSense.h"
#include <math.h>
#include <util/delay.h>
#include <avr/wdt.h> 
#include "arduino/BiscuitSerial.h"

#define BOARD_ADDR          0
#define LED_COUNT           6
#define TOUCH_COUNT         4
#define DE485_PIN           7
#define RE485_PIN           A5
#define GRN                 PD4
#define RED                 PD2
#define FRAME_COUNT         1

// Helper macros for frobbing bits
#define bitset(var,bitno) ((var) |= (1 << (bitno)))
#define bitclr(var,bitno) ((var) &= ~(1 << (bitno)))
#define bittst(var,bitno) (var& (1 << (bitno)))

const int _led_map[] = {9, 10, 11, 3, 5, 6};

/******************************************************************************
 ** EEPROM reads / writer helper functions
 ******************************************************************************/

uint8_t read_byte(int addr)
{
    return (uint8_t)EEPROM.read(addr);
}

void write_byte(int addr, uint8_t value)
{
    EEPROM.write(addr, value);
}

int read_int(int addr)
{
    unsigned char a = EEPROM.read(addr++);
    unsigned char b = EEPROM.read(addr);
    return static_cast<int>(a | (b << 8));
}

void write_int(int addr, int value)
{
    EEPROM.write(addr++, (value & 0xFF));
    EEPROM.write(addr, ((value >> 8) & 0xFF));
}

long read_long(int addr)
{
    unsigned char a = EEPROM.read(addr++);
    unsigned char b = EEPROM.read(addr++);
    unsigned char c = EEPROM.read(addr++);
    unsigned char d = EEPROM.read(addr);
    return static_cast<long>(a | 
            (static_cast<long>(b) << 8) | 
            (static_cast<long>(c) << 16) | 
            (static_cast<long>(d) << 24));
}

void write_long(int addr, long value)
{
    EEPROM.write(addr++, (value & 0xFF));
    EEPROM.write(addr++, ((value >> 8) & 0xFF));
    EEPROM.write(addr++, ((value >> 16) & 0xFF));
    EEPROM.write(addr, ((value >> 24) & 0xFF));
}


void enable_serial_output()
{
    // turn off receiver
    digitalWrite(RE485_PIN, HIGH);
    // turn on transmitter
    digitalWrite(DE485_PIN, HIGH);
    digitalWrite(GRN, HIGH);
}

void disable_serial_output()
{
    Serial.flush();
    delay(5);
    // turn off transmitter
    digitalWrite(DE485_PIN, LOW);
    // turn on receiver
    digitalWrite(RE485_PIN, LOW);
    digitalWrite(GRN, LOW);
}

/******************************************************************************
 ** Pin
 ******************************************************************************/

class Pin
{
public:
    void init(unsigned char pin)
    {
        _pin = pin;
        pinMode(_pin, OUTPUT);
    }

    void set(unsigned char val)
    {
        analogWrite(_pin, val);
    }

private:
    unsigned char _pin;
};


/******************************************************************************
 ** Globals
 ******************************************************************************/

#define LIGHT_MSG (LED_COUNT * FRAME_COUNT)

Pin             leds[LED_COUNT];
uint8_t         board_addr;
uint8_t         light_buffer[LIGHT_MSG];

/******************************************************************************
 ** Touch
 ******************************************************************************/

#define TOUCH_TIME 5

CapSense tch1 = CapSense(A0, A1);
CapSense tch2 = CapSense(A0, A2);
CapSense tch3 = CapSense(A0, A3);
CapSense tch4 = CapSense(A0, A4);

uint8_t get_touch_sample()
{
    static int touch_sensor = 0;
    uint16_t val;
    switch(touch_sensor)
    {
        case 0:
            val = tch1.capSense(TOUCH_TIME);
            break;
        case 1:
            val = tch2.capSense(TOUCH_TIME);
            break;
        case 2:
            val = tch3.capSense(TOUCH_TIME);
            break;
        case 3:
            val = tch4.capSense(TOUCH_TIME);
            break;
        default:
            val = 0;
    }
    touch_sensor = (touch_sensor + 1) % TOUCH_COUNT;
    return min(0x7f, val >> 1);
}

/******************************************************************************
 ** Setup
 ******************************************************************************/

void setup()
{
    // pins
    Serial.begin(1000000);
    pinMode(GRN, OUTPUT);
    pinMode(RED, OUTPUT);
    pinMode(DE485_PIN, OUTPUT);
    pinMode(RE485_PIN, OUTPUT);
    disable_serial_output();
    
    for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
    {
        leds[ch].init(_led_map[ch]);
        leds[ch].set(0);
    }
    
    board_addr = read_byte(BOARD_ADDR);
    /* blink out our board address */
    for (uint8_t addr = 0; addr <= board_addr; ++addr)
    {
        digitalWrite(GRN, HIGH);
        delay(300);
        digitalWrite(GRN, LOW);
        delay(300);
    }
        
    memset(light_buffer, 0, LIGHT_MSG * sizeof(char));
    digitalWrite(GRN, HIGH);
}

/******************************************************************************
 ** Main loop
 ******************************************************************************/

#define WAIT_FOR_COMMAND_STATE 0
#define COMMAND_STATE 1
#define COMMAND_ADDRESS_STATE 2
#define LIGHT_RECV_STATE 3
#define LIGHT_RECV_STATE_ACTUAL 4

#define BEACON_COMMAND 1
#define TOUCH_COMMAND 2

uint8_t light_buffer_idx = 0;
uint8_t serial_state = 0;
uint8_t serial_command = 0;
uint8_t command_address = 0;

void loop(void)
{
    if (!Serial.available()) 
        return;

    uint16_t lowhi = Serial.read();
    char ch = lowhi & 0xFF;
    char flags = (lowhi >> 8) & 0xFF;

    if (flags & PARITY_ERROR)
    {
        serial_state = WAIT_FOR_COMMAND_STATE;
        digitalWrite(RED, HIGH);
    } else
    if (ch & 0x80)
    {
        serial_state = COMMAND_STATE;
        ch = ch & 0x7F;
    }

    switch(serial_state)
    {
        case COMMAND_STATE:
            digitalWrite(RED, LOW);
            if (ch == 'L')
            {
                serial_command = LIGHT_RECV_STATE;
                serial_state = COMMAND_ADDRESS_STATE;
                light_buffer_idx = 0;
            } else
            if (ch == 'B')
            {
                serial_command = BEACON_COMMAND;
                serial_state = COMMAND_ADDRESS_STATE;
            } else
            if (ch == 'T')
            {
                serial_command = TOUCH_COMMAND;
                serial_state = COMMAND_ADDRESS_STATE;
            } else
            {
                /* ruh-roh */
                serial_state = WAIT_FOR_COMMAND_STATE;
            }
            break;
        case COMMAND_ADDRESS_STATE:
            command_address = ch;
            if (command_address == board_addr)
            {
                if (serial_command == BEACON_COMMAND)
                {
                    digitalWrite(RED, HIGH);
                    delay(300);
                    digitalWrite(RED, LOW);
                    serial_state = WAIT_FOR_COMMAND_STATE;
                } else
                if (serial_command == TOUCH_COMMAND)
                {
                    uint8_t val = get_touch_sample();
                    enable_serial_output();
                    Serial.write(val);
                    disable_serial_output();
                    serial_state = WAIT_FOR_COMMAND_STATE;
                } else
                if (serial_command == LIGHT_RECV_STATE)
                {
                    light_buffer_idx = 0;
                    serial_state = LIGHT_RECV_STATE_ACTUAL;
                }
            }
            serial_command = 0;
            break;
        case LIGHT_RECV_STATE_ACTUAL:
            light_buffer[light_buffer_idx++] = ch;
            if (light_buffer_idx >= LED_COUNT)
            {
                for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
                {
                    leds[ch].set(light_buffer[ch]);
                }
                serial_state = WAIT_FOR_COMMAND_STATE;
            }
            break;
    }

}

