#include <CapSense.h>
#include <string.h>

class Average
{
public:
    Average(uint8_t sz) :
        _sz(sz), _idx(0)
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
        return (sum / ((float)_sz));
    }

    void set(uint8_t offset)
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

CapSense   cs_4_8 = CapSense(A0, A1);
CapSense   cs_4_9 = CapSense(A0, A2);
CapSense   cs_4_10 = CapSense(A0, A3);
CapSense   cs_4_11 = CapSense(A0, A4);

Average    avg_4_8 = Average(10);
Average    avg_4_9 = Average(10);
Average    avg_4_10 = Average(10);
Average    avg_4_11 = Average(10);

void sample()
{
    avg_4_8.push(cs_4_8.capSense(25));
    avg_4_9.push(cs_4_9.capSense(25));
    avg_4_10.push(cs_4_10.capSense(25));
    avg_4_11.push(cs_4_11.capSense(25));
}

void setup()                    
{
    Serial.begin(9600);
    Serial.println("begin");
    while(!Serial.available())
    {
        sample();
    }
    // up
    Serial.println("up");
    while(!Serial.available())
    {
        sample();
    }
    Serial.read();
    Serial.println(avg_4_8.pull() + 0);
    avg_4_8.set(10);
    // down
    Serial.println("down");
    while(!Serial.available())
    {
        sample();
    }
    Serial.read();
    Serial.println(avg_4_9.pull() + 0);
    avg_4_9.set(10);
    // up
    Serial.println("left");
    while(!Serial.available())
    {
        sample();
    }
    Serial.read();
    Serial.println(avg_4_10.pull() + 0);
    avg_4_10.set(10);
    // up
    Serial.println("right");
    while(!Serial.available())
    {
        sample();
    }
    Serial.read();
    Serial.println(avg_4_11.pull() + 0);
    avg_4_11.set(10);
    Serial.println("done");
}

void loop()
{
    sample();
    if (avg_4_8.trigger())
    {
        Serial.println("up");
    }
    if (avg_4_9.trigger())
    {
        Serial.println("down");
    }
    if (avg_4_10.trigger())
    {
        Serial.println("left");
    }
    if (avg_4_11.trigger())
    {
        Serial.println("right");
    }
}
