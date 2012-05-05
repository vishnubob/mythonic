#include "arduino/Arduino.h"
#include "arduino/EEPROM.h"
#include <math.h>
#include <util/delay.h>
#include <avr/wdt.h> 

#define GRN PD4
#define RED PD2

#define TIMING_ADDR         0
#define SEED_ADDR           (TIMING_ADDR + (2 * sizeof(int) * LED_COUNT))
#define PROMPT_ENABLE       1
#define LED_COUNT           6

// Helper macros for frobbing bits
#define bitset(var,bitno) ((var) |= (1 << (bitno)))
#define bitclr(var,bitno) ((var) &= ~(1 << (bitno)))
#define bittst(var,bitno) (var& (1 << (bitno)))

const int _led_map[] = {9, 10, 11, 3, 5, 6};

/******************************************************************************
 ** EEPROM reads / writer helper functions
 ******************************************************************************/

int read_int(int &addr)
{
    unsigned char a = EEPROM.read(addr++);
    unsigned char b = EEPROM.read(addr++);
    return static_cast<int>(a | (b << 8));
}

void write_int(int &addr, int value)
{
    EEPROM.write(addr++, (value & 0xFF));
    EEPROM.write(addr++, ((value >> 8) & 0xFF));
}

long read_long(int &addr)
{
    unsigned char a = EEPROM.read(addr++);
    unsigned char b = EEPROM.read(addr++);
    unsigned char c = EEPROM.read(addr++);
    unsigned char d = EEPROM.read(addr++);
    return static_cast<long>(a | 
            (static_cast<long>(b) << 8) | 
            (static_cast<long>(c) << 16) | 
            (static_cast<long>(d) << 24));
}

void write_long(int &addr, long value)
{
    EEPROM.write(addr++, (value & 0xFF));
    EEPROM.write(addr++, ((value >> 8) & 0xFF));
    EEPROM.write(addr++, ((value >> 16) & 0xFF));
    EEPROM.write(addr++, ((value >> 24) & 0xFF));
}

unsigned long sync_random_seed()
{
    unsigned long seed;
    int addr;
    addr = SEED_ADDR;
    seed = static_cast<unsigned long>(read_long(addr));
    for(int pinidx = 0; pinidx < 6; ++pinidx)
    {
        seed <<= 3;
        seed ^= analogRead(pinidx);
    }
    addr = SEED_ADDR;
    write_long(addr, static_cast<long>(seed));
    randomSeed(seed);
    return seed;
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
 ** Ramp
 ******************************************************************************/

class Ramp
{
public:
    void init(int pt1, int pt2, unsigned long ttl, unsigned long delay=0, bool loop_flag=false, bool flip_flag=false)
    {
        _enable = false;
        _delay = 0;
        _loop_flag = loop_flag;
        _flip_flag = flip_flag;
        set_ramp(pt1, pt2, ttl);
    }

    void set_ramp(int pt1, int pt2, unsigned long ttl)
    {
        _pt1 = pt1;
        _pt2 = pt2;
        _ttl = ttl;
        set_clock();
    }

    void set_clock()
    {
        _timestamp = millis() + _delay;
        _slope = static_cast<float>(_pt2 - _pt1) / static_cast<float>(_ttl);
    }

    int step()
    {
        if (millis() < _timestamp)
        {
            return _value;
        }
        if (_enable) {
            if (timeout()) {
                _value = _pt2;
                _enable = _loop_flag;
                if (_flip_flag) {
                    flip();
                } else
                {
                    reset();
                }
            } else {
                _value = (millis() - _timestamp) * _slope + _pt1;
            }
        }
        return _value;
    }

    void print()
    {
        Serial.print(" [");
        Serial.print(_pt1, DEC);
        Serial.print("-");
        Serial.print(_pt2, DEC);
        Serial.print("]: ");
        Serial.print(_value, DEC);
        Serial.print(" delay: ");
        Serial.print(_delay, DEC);
        Serial.print(" ttl: ");
        Serial.print(_ttl, DEC);
        Serial.print(" flip: ");
        Serial.print(_flip_flag, DEC);
        Serial.print(" loop: ");
        Serial.print(_loop_flag, DEC);
        Serial.print(" en: ");
        Serial.println(_enable, DEC);
    }

    void flip() { set_ramp(_pt2, _pt1, _ttl); }
    void reset() { set_ramp(_pt1, _pt2, _ttl); }
    void enable() { _enable = true; reset(); }
    void disable()  { _enable = false; }
    bool is_enabled()  { return _enable; }
    void set_delay(unsigned long delay) { _delay = delay; }
    void set_flip(bool flag) { _flip_flag = flag; }
    void set_loop(bool flag) { _loop_flag = flag; }
    void set_pt1(int pt1) { _pt1 = pt1; reset(); }
    void set_pt2(int pt2) { _pt2 = pt2; reset(); }
    void set_ttl(unsigned long ttl) { _ttl = ttl; reset(); }
    bool timeout() { return ((millis() - _timestamp) >= _ttl); }
    int get_value() { return _value; }

private:
    int _pt1;
    int _pt2;
    int _value;
    unsigned long _ttl;
    unsigned long _delay;
    unsigned long _timestamp;
    float _slope;
    bool _enable;
    bool _flip_flag;
    bool _loop_flag;
};

/******************************************************************************
 ** Globals
 ******************************************************************************/

Ramp            ramps[LED_COUNT];
Pin             leds[LED_COUNT];

/******************************************************************************
 ** Setup
 ******************************************************************************/

void setup()
{
    Serial.begin(57600);
    Serial.print("[");
    
    // priming
    Serial.print("init ...");
    Serial.println("]");
    Serial.flush();

    // init
    Serial.println("init done!");

    for(uint8_t ch = 0; ch < LED_COUNT; ++ch)
    {
        leds[ch].init(_led_map[ch]);
    }
}


/******************************************************************************
 ** Serial
 ******************************************************************************/

#if PROMPT_ENABLE
void Prompt(void)
{
  static long v = 0;
  static unsigned char channel = 0;
  bool echo_on = true;

  //Serial.println((Serial.available() ? "Y" : "N"));
  if (Serial.available()) {
    char ch = Serial.read();

    switch(ch) {
      case '0'...'9':
        v = v * 10 + ch - '0';
        break;
      case '-':
        v *= -1;
        break;
      case 'z':
        v = 0;
        break;
      case '&':
        Serial.print("!");
        echo_on = false;
        break;
      case 'W':
        for (uint8_t idx = 0; idx < LED_COUNT; ++idx)
        {
            while (!Serial.available()) {}
            leds[idx].set(Serial.read());
        }
        echo_on = false;
        break;
      case 's':
        leds[channel].set(v);
        v = 0;
        break;
      case 'C':
        channel = v;
        Serial.println("");
        Serial.println("channel set");
        v = 0;
        break;
      case 'd':
        ramps[channel].set_delay(v);
        v = 0;
        Serial.println("");
        Serial.println("delay set");
        break;
      case 'o':
        ramps[channel].set_pt1(v);
        Serial.println("");
        Serial.println("pt1 set");
        v = 0;
        break;
      case 'O':
        ramps[channel].set_pt2(v);
        Serial.println("");
        Serial.println("pt2 set");
        v = 0;
        break;
      case 'T':
        ramps[channel].set_ttl(v);
        Serial.println("");
        Serial.println("ttl set");
        v = 0;
        break;
      case 'F':
        ramps[channel].set_flip(true);
        Serial.println("");
        Serial.println("flip on");
        break;
      case 'f':
        ramps[channel].set_flip(false);
        Serial.println("");
        Serial.println("flip off");
        break;
      case 'L':
        ramps[channel].set_loop(true);
        Serial.println("");
        Serial.println("loop on");
        break;
      case 'l':
        ramps[channel].set_loop(false);
        Serial.println("");
        Serial.println("loop off");
        break;
      case 'E':
        ramps[channel].enable();
        Serial.println("");
        Serial.println("enabled");
        break;
      case 'e':
        ramps[channel].disable();
        Serial.println("");
        Serial.println("disabled");
        break;
      case 'g':
        for (uint8_t idx = 0; idx < LED_COUNT; ++idx)
        {
            ramps[idx].set_clock();
            ramps[idx].enable();
        }
        break;
      case 'x':
        for (uint8_t idx = 0; idx < LED_COUNT; ++idx)
        {
            ramps[idx].disable();
            leds[idx].set(0);
        }
        break;
      case 'p':
        Serial.println("");
        for (uint8_t idx = 0; idx < LED_COUNT; ++idx)
        {
            Serial.print(idx, DEC);
            Serial.print(": ");
            ramps[idx].print();
        }
        break;
      default:
        Serial.print("Unknown command: ");
        Serial.println(ch, DEC);
    }
    if (echo_on)
    {
        Serial.println("");
        Serial.print("Value: ");
        Serial.print(v, DEC);
        Serial.print(" - Channel: ");
        Serial.print(channel, DEC);
        Serial.print(" - millis: ");
        Serial.println(millis(), DEC);
        Serial.print("> ");
    }
  }
}
#endif // PROMPT_ENABLE

/******************************************************************************
 ** Main loop
 ******************************************************************************/

void loop()
{
    // enable the watchdog timer, 8 seconds
    wdt_enable(WDTO_8S);
    for(;;)
    {
        wdt_reset();
        for (uint8_t ch = 0; ch < LED_COUNT; ++ch)
        {
            if (ramps[ch].is_enabled())
            {
                leds[ch].set(ramps[ch].step());
            }
        }
        wdt_reset();
#if PROMPT_ENABLE
        Prompt();
#endif // PROMPT_ENABLE
    }
}
