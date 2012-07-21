#include "arduino/Arduino.h"
#include "arduino/EEPROM.h"
#include "CapSense/CapSense.h"
#include <math.h>
#include <util/delay.h>
#include <avr/wdt.h> 
#include <compat/deprecated.h>
#include "board_address.h"

#define LED_COUNT           6
#define TOUCH_COUNT         4
#define DE485_PIN           7
#define RE485_PIN           A5
#define GRN                 PD4
#define RED                 PD2
#define FRAME_COUNT         1
#define BAUD_RATE           1000000

// Helper macros for frobbing bits
#define bitset(var,bitno) ((var) |= (1 << (bitno)))
#define bitclr(var,bitno) ((var) &= ~(1 << (bitno)))
#define bittst(var,bitno) (var& (1 << (bitno)))

const int _led_map[] = {9, 10, 11, 3, 5, 6};

/******************************************************************************
 ** serial read / writer helper functions
 ******************************************************************************/

void disable_rs485()
{
    // turn off receiver
    digitalWrite(RE485_PIN, HIGH);
    // turn off transmitter
    digitalWrite(DE485_PIN, LOW);
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
    // XXX: DELAY
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
 ** Touch
 ******************************************************************************/

#define TOUCH_SAMPLES 100

class Average
{
public:
    Average() {}

    Average(uint8_t sz) :
        _sz(8), _idx(0)
    {
        _data = (unsigned long*)malloc(_sz * sizeof(unsigned long));
        memset(_data, 0, _sz * sizeof(unsigned long));
    }

    void push(unsigned long val)
    {
        _data[_idx] = val;
        _idx = (_idx + 1) % _sz;
    }

    unsigned long pull()
    {
        unsigned long sum = 0;
        for(uint8_t sum_idx = 0; sum_idx < _sz; ++sum_idx)
        {
            sum += _data[sum_idx];
        }
        return (sum << 3);
    }

    void set(unsigned long offset)
    {
        _level = pull() + offset;
    }

    bool trigger()
    {
        return (pull() > _level);
    }

private:
    uint8_t _sz;
    uint8_t _idx;
    unsigned long* _data;
    unsigned long _level;
};

class TouchSet
{
public:
    TouchSet()
    {
        _sensors[0] = CapSense(A0, A1);
        _sensors[1] = CapSense(A0, A2);
        _sensors[2] = CapSense(A0, A3);
        _sensors[3] = CapSense(A0, A4);
        _average[0] = Average(20);
        _average[1] = Average(20);
        _average[2] = Average(20);
        _average[3] = Average(20);
        _sensor_idx = 0;
        _last_cal = 0;
        _timeout_cal = 200;
    }

    void step()
    {
        CapSense *current_sensor = _sensors + _sensor_idx;
        if (current_sensor->step_sensor())
        {
            _average[_sensor_idx].push(current_sensor->get_current_value());
            _sensor_idx = (_sensor_idx + 1) % TOUCH_COUNT;
        }
    }

    bool trigger()
    {
        bool trigger_flag = false;
        for(int x = 0; x < TOUCH_COUNT; ++x)
        {
            trigger_flag |= _average[x].trigger();
        }

        if ((_last_cal - millis()) > _timeout_cal)
        {
            for(int x = 0; x < TOUCH_COUNT; ++x)
            {
                _average[x].set(50);
            }
            _last_cal = millis();
        }
        return trigger_flag;
    }

private:
    CapSense _sensors[TOUCH_COUNT];
    Average _average[TOUCH_COUNT];
    unsigned long _last_cal;
    unsigned long _timeout_cal;
    volatile uint8_t _sensor_idx;
};

/******************************************************************************
 ** Globals
 ******************************************************************************/

// since everything is transmitted in 7bits (data wise)
// we use an extra frame for the 6 missing bits for each 
// channel.
#define LIGHT_MSG (LED_COUNT * FRAME_COUNT + 1)

Pin             leds[LED_COUNT];
TouchSet        touchset;
uint8_t         board_addr;
uint8_t         light_buffer[LIGHT_MSG];

/******************************************************************************
 ** Setup
 ******************************************************************************/

void setup()
{
    // pins
    Serial.begin(BAUD_RATE);
    pinMode(GRN, OUTPUT);
    pinMode(RED, OUTPUT);
    pinMode(DE485_PIN, OUTPUT);
    pinMode(RE485_PIN, OUTPUT);
    disable_serial_output();
    
    // init the LEDs
    memset(light_buffer, 0, LIGHT_MSG * sizeof(char));
    for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
    {
        leds[ch].init(_led_map[ch]);
        leds[ch].set(0);
    }
    
    // BOARD_ADDR is defined by a macro, 
    // usually built on the fly by burn.py
    board_addr = BOARD_ADDR;

    // enable timer2 overflow interrupt
    // for touch sensors
    sbi(TIMSK2, TOIE2);

    /* blink */
    digitalWrite(GRN, HIGH);
    delay(300);
    digitalWrite(GRN, LOW);
    delay(300);
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

    char ch = Serial.read();

    if (ch & 0x80)
    {
        serial_state = COMMAND_STATE;
        ch = ch & 0x7F;
    }

    switch(serial_state)
    {
        digitalWrite(RED, LOW);
        case COMMAND_STATE:
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
                    enable_serial_output();
                    Serial.write((uint8_t)touchset.trigger());
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
            if (light_buffer_idx >= (LED_COUNT + 1))
            {
                for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
                {
                    uint8_t val = (light_buffer[ch] << 1) | ((light_buffer[LED_COUNT] & (1 << (LED_COUNT - ch))) >> (LED_COUNT - ch));
                    leds[ch].set(val);
                }
                serial_state = WAIT_FOR_COMMAND_STATE;
            }
            break;
    }
}

SIGNAL(TIMER2_OVF_vect)
{
    touchset.step();
}
