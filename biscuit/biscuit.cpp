#include "arduino/Arduino.h"
#include "arduino/EEPROM.h"
#include "CapSense/CapSense.h"
#include <math.h>
#include <util/delay.h>
#include <avr/wdt.h> 

#define GRN PD4
#define RED PD2

#define BOARD_ADDR          0
#define PROMPT_ENABLE       1
#define LED_COUNT           6
#define DE485_PIN           7
#define TOUCH_INTERVAL      25
#define RE485_PIN           A5

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

#define LIGHT_MSG (LED_COUNT * 7)
#define TOUCH_MSG 1

Pin             leds[LED_COUNT];
uint8_t         board_addr;
uint8_t         light_buffer[LIGHT_MSG];


/* touch */

class Average
{
public:
    Average(uint8_t sz) :
        _sz(8), _idx(0)
    {
        _data = (long*)malloc(_sz * sizeof(long));
        memset(_data, 0, _sz * sizeof(long));
    }

    void push(long val)
    {
        _data[_idx] = val;
        _idx = (_idx + 1) % _sz;
    }

    long pull()
    {
        long sum = 0;
        for(uint8_t sum_idx = 0; sum_idx < _sz; ++sum_idx)
        {
            sum += _data[sum_idx];
        }
        return (sum >> 3);
    }

    void set(long offset)
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
    long* _data;
    long _level;
};

CapSense   tch1 = CapSense(A0, A1);
CapSense   tch2 = CapSense(A0, A2);
CapSense   tch3 = CapSense(A0, A3);
CapSense   tch4 = CapSense(A0, A4);

Average    avg_tch1 = Average(8);
Average    avg_tch2 = Average(8);
Average    avg_tch3 = Average(8);
Average    avg_tch4 = Average(8);

void sample_touch_sensors()
{
    avg_tch1.push(tch1.capSense(5));
    avg_tch2.push(tch2.capSense(5));
    avg_tch3.push(tch3.capSense(5));
    avg_tch4.push(tch4.capSense(5));
}

bool trigger_touch_sensors()
{
    return (avg_tch1.trigger() || avg_tch2.trigger() || avg_tch3.trigger() || avg_tch4.trigger());
}

void normalize_touch_sensors()
{
    for(int x = 0; x < 10; ++x)
    {
        sample_touch_sensors();
        delay(100);
    }
    avg_tch1.set(500);
    avg_tch2.set(500);
    avg_tch3.set(500);
    avg_tch4.set(500);
}

/******************************************************************************
 ** Setup
 ******************************************************************************/

void setup()
{
    // pins
    Serial.begin(250000);
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
    //board_addr = 4;
    for (uint8_t addr = 0; addr <= board_addr; ++addr)
    {
        digitalWrite(GRN, HIGH);
        delay(300);
        digitalWrite(GRN, LOW);
        delay(300);
    }
        
    memset(light_buffer, 0, LIGHT_MSG * sizeof(char));
    normalize_touch_sensors();
    digitalWrite(GRN, HIGH);
}


/******************************************************************************
 ** Serial
 ******************************************************************************/

void poll_input(void)
{
    if (Serial.available()) 
    {
        char ch = Serial.read();
        if (ch == 'L')
        {
            for(uint8_t idx = 0; idx < LIGHT_MSG; ++idx)
            {
                while (!Serial.available()) {}
                light_buffer[idx] = Serial.read();
                //Serial.println(light_buffer[idx], DEC);
            }
        } else
        if (ch == 'T')
        {
            // toss this
            while (!Serial.available()) {}
            Serial.read();
        } else
        if (ch == 'R')
        {
            while (!Serial.available()) {}
            uint8_t addr = Serial.read();
            if (addr == board_addr)
            {
                digitalWrite(RED, !digitalRead(RED));
            }
        } else
        if (ch == 'Z')
        {
            for(uint8_t idx = 0; idx < LIGHT_MSG; ++idx)
            {
                light_buffer[idx] = 0;
            }
        }
    }
}

/******************************************************************************
 ** Main loop
 ******************************************************************************/

void loop()
{
    static int interval = 0;

    poll_input();
    for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
    {
        leds[ch].set(light_buffer[ch + (LED_COUNT * board_addr)]);
        //leds[ch].set(light_buffer[ch]);
    }

    /*
    interval = (interval + 1) % TOUCH_INTERVAL;
    if (interval == 0)
    {
        sample_touch_sensors();
        if (trigger_touch_sensors())
        {
            enable_serial_output();
            Serial.write('T');
            Serial.flush();
            Serial.write(board_addr);
            disable_serial_output();
        }
    }
    */
}
