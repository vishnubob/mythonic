EESchema Schematic File Version 2  date Sun 11 Mar 2012 03:06:23 AM EDT
LIBS:power,device,transistors,conn,linear,regul,74xx,cmos4000,adc-dac,memory,xilinx,special,microcontrollers,dsp,microchip,analog_switches,motorola,texas,intel,audio,interface,digital-audio,philips,display,cypress,siliconi,opto,atmel,contrib,valves
EELAYER 43  0
EELAYER END
$Descr A4 11700 8267
Sheet 1 1
Title ""
Date "11 mar 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Connection ~ 3900 3300
$Comp
L VAA #PWR?
U 1 1 4F5C4ECC
P 3900 3300
F 0 "#PWR?" H 3900 3360 30  0001 C CNN
F 1 "VAA" H 3900 3410 30  0000 C CNN
	1    3900 3300
	1    0    0    -1  
$EndComp
Connection ~ 5550 3300
$Comp
L +5V #PWR?
U 1 1 4F5C4E81
P 5550 3300
F 0 "#PWR?" H 5550 3390 20  0001 C CNN
F 1 "+5V" H 5550 3390 30  0000 C CNN
	1    5550 3300
	1    0    0    -1  
$EndComp
Connection ~ 4750 3900
$Comp
L GND #PWR?
U 1 1 4F5C4E38
P 4750 3900
F 0 "#PWR?" H 4750 3900 30  0001 C CNN
F 1 "GND" H 4750 3830 30  0001 C CNN
	1    4750 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 3300 3900 3300
Connection ~ 4350 3300
Connection ~ 4350 3700
Connection ~ 4750 3700
Connection ~ 5150 3300
Connection ~ 4750 3600
Connection ~ 5150 3700
Wire Wire Line
	4750 3600 4750 3900
Wire Wire Line
	4350 3700 5150 3700
Wire Wire Line
	5550 3300 5150 3300
$Comp
L C C?
U 1 1 4F5C4CA3
P 5150 3500
F 0 "C?" H 5200 3600 50  0000 L CNN
F 1 "C" H 5200 3400 50  0000 L CNN
	1    5150 3500
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 4F5C4C99
P 4350 3500
F 0 "C?" H 4400 3600 50  0000 L CNN
F 1 "C" H 4400 3400 50  0000 L CNN
	1    4350 3500
	1    0    0    -1  
$EndComp
$Comp
L 7805 U?
U 1 1 4F5C4BF3
P 4750 3300
F 0 "U?" H 4900 3060 60  0000 C CNN
F 1 "7805" H 4755 3440 60  0000 C CNN
	1    4750 3300
	1    0    0    -1  
$EndComp
$EndSCHEMATC
