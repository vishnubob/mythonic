EESchema Schematic File Version 2  date 3/26/2012 1:52:50 AM
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Atmega168
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "26 mar 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 2950 4100 0    60   ~ 0
PD6
Wire Wire Line
	3100 4100 3100 4250
Connection ~ 3200 4750
Wire Wire Line
	3200 4750 3200 4600
Wire Wire Line
	3200 4600 3500 4600
Wire Wire Line
	3500 4600 3500 4550
Wire Wire Line
	3850 4850 3850 4750
Wire Wire Line
	3850 4750 3700 4750
Wire Wire Line
	3700 4250 4000 4250
Wire Wire Line
	4000 4250 4000 5050
Wire Wire Line
	4000 5050 3500 5050
Connection ~ 3850 4250
Wire Wire Line
	3100 4750 3300 4750
Wire Wire Line
	3300 4100 3300 4250
Text Label 3250 4100 0    60   ~ 0
CH2
$Comp
L GND #PWR?
U 1 1 4F7003C8
P 3850 4850
F 0 "#PWR?" H 3850 4850 30  0001 C CNN
F 1 "GND" H 3850 4780 30  0001 C CNN
	1    3850 4850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F7003C7
P 3850 4500
F 0 "R?" V 3930 4500 50  0000 C CNN
F 1 "R" V 3850 4500 50  0000 C CNN
	1    3850 4500
	-1   0    0    1   
$EndComp
$Comp
L R R?
U 1 1 4F7003C6
P 3100 4500
F 0 "R?" V 3180 4500 50  0000 C CNN
F 1 "R" V 3100 4500 50  0000 C CNN
	1    3100 4500
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q?
U 1 1 4F7003C5
P 3500 4850
F 0 "Q?" V 3500 5050 50  0000 C CNN
F 1 "NPN" V 3500 4650 50  0000 C CNN
F 2 "TO92-EBC" H 3690 4850 30  0001 C CNN
	1    3500 4850
	0    -1   -1   0   
$EndComp
$Comp
L MOSFET_P Q?
U 1 1 4F7003C4
P 3500 4350
F 0 "Q?" V 3350 4550 60  0000 R CNN
F 1 "FET" V 3350 4300 60  0000 R CNN
	1    3500 4350
	0    -1   -1   0   
$EndComp
$Comp
L MOSFET_P Q?
U 1 1 4F7003C2
P 4700 4450
F 0 "Q?" V 4550 4650 60  0000 R CNN
F 1 "FET" V 4550 4400 60  0000 R CNN
	1    4700 4450
	0    -1   -1   0   
$EndComp
$Comp
L BC237 Q?
U 1 1 4F7003C1
P 4700 4950
F 0 "Q?" V 4700 5150 50  0000 C CNN
F 1 "NPN" V 4700 4750 50  0000 C CNN
F 2 "TO92-EBC" H 4890 4950 30  0001 C CNN
	1    4700 4950
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 4F7003C0
P 4300 4600
F 0 "R?" V 4380 4600 50  0000 C CNN
F 1 "R" V 4300 4600 50  0000 C CNN
	1    4300 4600
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F7003BF
P 5050 4600
F 0 "R?" V 5130 4600 50  0000 C CNN
F 1 "R" V 5050 4600 50  0000 C CNN
	1    5050 4600
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR?
U 1 1 4F7003BE
P 5050 4950
F 0 "#PWR?" H 5050 4950 30  0001 C CNN
F 1 "GND" H 5050 4880 30  0001 C CNN
	1    5050 4950
	1    0    0    -1  
$EndComp
Text Label 4450 4200 0    60   ~ 0
CH3
Wire Wire Line
	4500 4200 4500 4350
Wire Wire Line
	4300 4850 4500 4850
Connection ~ 5050 4350
Wire Wire Line
	5200 5150 4700 5150
Wire Wire Line
	5200 4350 5200 5150
Wire Wire Line
	4900 4350 5200 4350
Wire Wire Line
	5050 4850 4900 4850
Wire Wire Line
	5050 4950 5050 4850
Wire Wire Line
	4700 4700 4700 4650
Wire Wire Line
	4400 4700 4700 4700
Wire Wire Line
	4400 4850 4400 4700
Connection ~ 4400 4850
Wire Wire Line
	4300 4200 4300 4350
Text Label 4150 4200 0    60   ~ 0
PB3
Text Label 3000 5450 0    60   ~ 0
PB1
Wire Wire Line
	3150 5450 3150 5600
Connection ~ 3250 6100
Wire Wire Line
	3250 6100 3250 5950
Wire Wire Line
	3250 5950 3550 5950
Wire Wire Line
	3550 5950 3550 5900
Wire Wire Line
	3900 6200 3900 6100
Wire Wire Line
	3900 6100 3750 6100
Wire Wire Line
	3750 5600 4050 5600
Wire Wire Line
	4050 5600 4050 6400
Wire Wire Line
	4050 6400 3550 6400
Connection ~ 3900 5600
Wire Wire Line
	3150 6100 3350 6100
Wire Wire Line
	3350 5450 3350 5600
Text Label 3300 5450 0    60   ~ 0
CH5
$Comp
L GND #PWR?
U 1 1 4F7003BD
P 3900 6200
F 0 "#PWR?" H 3900 6200 30  0001 C CNN
F 1 "GND" H 3900 6130 30  0001 C CNN
	1    3900 6200
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F7003BC
P 3900 5850
F 0 "R?" V 3980 5850 50  0000 C CNN
F 1 "R" V 3900 5850 50  0000 C CNN
	1    3900 5850
	-1   0    0    1   
$EndComp
$Comp
L R R?
U 1 1 4F7003BB
P 3150 5850
F 0 "R?" V 3230 5850 50  0000 C CNN
F 1 "R" V 3150 5850 50  0000 C CNN
	1    3150 5850
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q?
U 1 1 4F7003BA
P 3550 6200
F 0 "Q?" V 3550 6400 50  0000 C CNN
F 1 "NPN" V 3550 6000 50  0000 C CNN
F 2 "TO92-EBC" H 3740 6200 30  0001 C CNN
	1    3550 6200
	0    -1   -1   0   
$EndComp
$Comp
L MOSFET_P Q?
U 1 1 4F7003B9
P 3550 5700
F 0 "Q?" V 3400 5900 60  0000 R CNN
F 1 "FET" V 3400 5650 60  0000 R CNN
	1    3550 5700
	0    -1   -1   0   
$EndComp
$Comp
L MOSFET_P Q?
U 1 1 4F7003B8
P 2100 5650
F 0 "Q?" V 1950 5850 60  0000 R CNN
F 1 "FET" V 1950 5600 60  0000 R CNN
	1    2100 5650
	0    -1   -1   0   
$EndComp
$Comp
L BC237 Q?
U 1 1 4F7003B7
P 2100 6150
F 0 "Q?" V 2100 6350 50  0000 C CNN
F 1 "NPN" V 2100 5950 50  0000 C CNN
F 2 "TO92-EBC" H 2290 6150 30  0001 C CNN
	1    2100 6150
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 4F7003B6
P 1700 5800
F 0 "R?" V 1780 5800 50  0000 C CNN
F 1 "R" V 1700 5800 50  0000 C CNN
	1    1700 5800
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F7003B5
P 2450 5800
F 0 "R?" V 2530 5800 50  0000 C CNN
F 1 "R" V 2450 5800 50  0000 C CNN
	1    2450 5800
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR?
U 1 1 4F7003B4
P 2450 6150
F 0 "#PWR?" H 2450 6150 30  0001 C CNN
F 1 "GND" H 2450 6080 30  0001 C CNN
	1    2450 6150
	1    0    0    -1  
$EndComp
Text Label 1850 5400 0    60   ~ 0
CH4
Wire Wire Line
	1900 5400 1900 5550
Wire Wire Line
	1700 6050 1900 6050
Connection ~ 2450 5550
Wire Wire Line
	2600 6350 2100 6350
Wire Wire Line
	2600 5550 2600 6350
Wire Wire Line
	2300 5550 2600 5550
Wire Wire Line
	2450 6050 2300 6050
Wire Wire Line
	2450 6150 2450 6050
Wire Wire Line
	2100 5900 2100 5850
Wire Wire Line
	1800 5900 2100 5900
Wire Wire Line
	1800 6050 1800 5900
Connection ~ 1800 6050
Wire Wire Line
	1700 5400 1700 5550
Text Label 1550 5400 0    60   ~ 0
PB2
Text Label 1500 3950 0    60   ~ 0
PD5
Wire Wire Line
	1650 3950 1650 4100
Connection ~ 1750 4600
Wire Wire Line
	1750 4600 1750 4450
Wire Wire Line
	1750 4450 2050 4450
Wire Wire Line
	2050 4450 2050 4400
Wire Wire Line
	2400 4700 2400 4600
Wire Wire Line
	9350 950  9350 1050
Wire Wire Line
	9350 1050 9100 1050
Wire Wire Line
	8600 1050 8300 1050
Wire Wire Line
	8300 1050 8300 1600
Connection ~ 8300 1600
Wire Wire Line
	10600 1400 10600 1250
Wire Wire Line
	9800 1500 9700 1500
Wire Wire Line
	9700 1500 9700 3000
Wire Wire Line
	9700 3000 9600 3000
Wire Wire Line
	9800 1600 8100 1600
Wire Wire Line
	8100 1600 8100 2100
Wire Wire Line
	7950 3900 7950 2800
Wire Wire Line
	7950 2800 8100 2800
Wire Wire Line
	9950 2600 9950 2700
Wire Wire Line
	9950 2700 9600 2700
Wire Wire Line
	7050 2600 7050 3200
Connection ~ 7500 2600
Wire Wire Line
	7250 2600 7800 2600
Wire Wire Line
	7800 2600 7800 2900
Wire Wire Line
	7800 2900 8100 2900
Wire Wire Line
	2750 1150 2350 1150
Wire Wire Line
	1550 1550 2350 1550
Wire Wire Line
	1950 1450 1950 1750
Connection ~ 2350 1550
Connection ~ 1950 1450
Connection ~ 2350 1150
Connection ~ 1950 1550
Connection ~ 1550 1550
Connection ~ 1550 1150
Wire Wire Line
	1550 1150 1100 1150
Connection ~ 1950 1750
Connection ~ 2750 1150
Connection ~ 1100 1150
Wire Wire Line
	8100 3000 7800 3000
Wire Wire Line
	7800 3000 7800 3200
Wire Wire Line
	7800 3200 7250 3200
Connection ~ 7500 3200
Wire Wire Line
	6850 2950 6850 2900
Wire Wire Line
	6850 2900 7050 2900
Connection ~ 7050 2900
Wire Wire Line
	9600 2900 9950 2900
Wire Wire Line
	9950 2900 9950 3000
Wire Wire Line
	8100 2700 7950 2700
Wire Wire Line
	7950 2700 7950 1700
Wire Wire Line
	9600 3100 9750 3100
Wire Wire Line
	9750 3100 9750 1400
Wire Wire Line
	9750 1400 9800 1400
Wire Wire Line
	9600 3200 10800 3200
Wire Wire Line
	10800 3200 10800 1500
Wire Wire Line
	10800 1500 10600 1500
Wire Wire Line
	10600 1600 10600 1750
Wire Wire Line
	9200 1300 9350 1300
Wire Wire Line
	9350 1300 9350 1200
Wire Wire Line
	8600 1300 8300 1300
Connection ~ 8300 1300
Wire Wire Line
	2400 4600 2250 4600
Wire Wire Line
	2250 4100 2550 4100
Wire Wire Line
	2550 4100 2550 4900
Wire Wire Line
	2550 4900 2050 4900
Connection ~ 2400 4100
Wire Wire Line
	1650 4600 1850 4600
Wire Wire Line
	1850 3950 1850 4100
Text Label 1800 3950 0    60   ~ 0
CH1
$Comp
L GND #PWR?
U 1 1 4F700248
P 2400 4700
F 0 "#PWR?" H 2400 4700 30  0001 C CNN
F 1 "GND" H 2400 4630 30  0001 C CNN
	1    2400 4700
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F700111
P 2400 4350
F 0 "R?" V 2480 4350 50  0000 C CNN
F 1 "R" V 2400 4350 50  0000 C CNN
	1    2400 4350
	-1   0    0    1   
$EndComp
$Comp
L R R?
U 1 1 4F700110
P 1650 4350
F 0 "R?" V 1730 4350 50  0000 C CNN
F 1 "R" V 1650 4350 50  0000 C CNN
	1    1650 4350
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q?
U 1 1 4F70010B
P 2050 4700
F 0 "Q?" V 2050 4900 50  0000 C CNN
F 1 "NPN" V 2050 4500 50  0000 C CNN
F 2 "TO92-EBC" H 2240 4700 30  0001 C CNN
	1    2050 4700
	0    -1   -1   0   
$EndComp
$Comp
L MOSFET_P Q?
U 1 1 4F700103
P 2050 4200
F 0 "Q?" V 1900 4400 60  0000 R CNN
F 1 "FET" V 1900 4150 60  0000 R CNN
	1    2050 4200
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 4F6FF95D
P 9350 1200
F 0 "#PWR?" H 9350 1200 30  0001 C CNN
F 1 "GND" H 9350 1130 30  0001 C CNN
	1    9350 1200
	-1   0    0    1   
$EndComp
$Comp
L +5V #PWR?
U 1 1 4F6FF97B
P 9350 950
F 0 "#PWR?" H 9350 1040 20  0001 C CNN
F 1 "+5V" H 9350 1040 30  0000 C CNN
	1    9350 950 
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 4F6FF92D
P 10600 1750
F 0 "#PWR?" H 10600 1750 30  0001 C CNN
F 1 "GND" H 10600 1680 30  0001 C CNN
	1    10600 1750
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 4F6FF91F
P 10600 1250
F 0 "#PWR?" H 10600 1340 20  0001 C CNN
F 1 "+5V" H 10600 1340 30  0000 C CNN
	1    10600 1250
	1    0    0    -1  
$EndComp
$Comp
L CONN_3X2 P?
U 1 1 4F6FF84A
P 10200 1550
F 0 "P?" H 10200 1800 50  0000 C CNN
F 1 "CONN_3X2" V 10200 1600 40  0000 C CNN
	1    10200 1550
	1    0    0    -1  
$EndComp
$Comp
L SW_PUSH SW?
U 1 1 4F6FF829
P 8900 1300
F 0 "SW?" H 9050 1410 50  0000 C CNN
F 1 "SW_PUSH" H 8900 1220 50  0000 C CNN
	1    8900 1300
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 4F6FF538
P 8850 1050
F 0 "R?" V 8930 1050 50  0000 C CNN
F 1 "R" V 8850 1050 50  0000 C CNN
	1    8850 1050
	0    -1   -1   0   
$EndComp
$Comp
L +5V #PWR?
U 1 1 4F6FF4B9
P 7950 1700
F 0 "#PWR?" H 7950 1790 20  0001 C CNN
F 1 "+5V" H 7950 1790 30  0000 C CNN
	1    7950 1700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 4F6FF489
P 7950 3900
F 0 "#PWR?" H 7950 3900 30  0001 C CNN
F 1 "GND" H 7950 3830 30  0001 C CNN
	1    7950 3900
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 4F6FF453
P 9950 3000
F 0 "#PWR?" H 9950 3090 20  0001 C CNN
F 1 "+5V" H 9950 3090 30  0000 C CNN
	1    9950 3000
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR?
U 1 1 4F6FF445
P 9950 2600
F 0 "#PWR?" H 9950 2600 30  0001 C CNN
F 1 "GND" H 9950 2530 30  0001 C CNN
	1    9950 2600
	-1   0    0    1   
$EndComp
$Comp
L CSMALL C?
U 1 1 4F6FF2EC
P 9950 2800
F 0 "C?" H 9975 2850 30  0000 L CNN
F 1 "CSMALL" H 9975 2750 30  0000 L CNN
	1    9950 2800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 4F6FF2A4
P 6850 2950
F 0 "#PWR?" H 6850 2950 30  0001 C CNN
F 1 "GND" H 6850 2880 30  0001 C CNN
	1    6850 2950
	1    0    0    -1  
$EndComp
$Comp
L CSMALL C?
U 1 1 4F6FF269
P 7150 3200
F 0 "C?" H 7175 3250 30  0000 L CNN
F 1 "CSMALL" H 7175 3150 30  0000 L CNN
	1    7150 3200
	0    -1   -1   0   
$EndComp
$Comp
L CSMALL C?
U 1 1 4F6FF263
P 7150 2600
F 0 "C?" H 7175 2650 30  0000 L CNN
F 1 "CSMALL" H 7175 2550 30  0000 L CNN
	1    7150 2600
	0    -1   -1   0   
$EndComp
$Comp
L CRYSTAL X?
U 1 1 4F6FF180
P 7500 2900
F 0 "X?" H 7500 3050 60  0000 C CNN
F 1 "CRYSTAL" H 7500 2750 60  0000 C CNN
	1    7500 2900
	0    -1   -1   0   
$EndComp
$Comp
L ATMEGA168 U?
U 1 1 4F6FF0D4
P 8850 2750
F 0 "U?" H 8850 2650 50  0000 C CNN
F 1 "ATMEGA168" H 8850 2850 50  0000 C CNN
F 2 "MODULE" H 8850 2750 50  0001 C CNN
F 3 "DOCUMENTATION" H 8850 2750 50  0001 C CNN
	1    8850 2750
	1    0    0    -1  
$EndComp
$Comp
L VAA #PWR?
U 1 1 4F5C4ECC
P 1100 1150
F 0 "#PWR?" H 1100 1210 30  0001 C CNN
F 1 "VAA" H 1100 1260 30  0000 C CNN
	1    1100 1150
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 4F5C4E81
P 2750 1150
F 0 "#PWR?" H 2750 1240 20  0001 C CNN
F 1 "+5V" H 2750 1240 30  0000 C CNN
	1    2750 1150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 4F5C4E38
P 1950 1750
F 0 "#PWR?" H 1950 1750 30  0001 C CNN
F 1 "GND" H 1950 1680 30  0001 C CNN
	1    1950 1750
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 4F5C4CA3
P 2350 1350
F 0 "C?" H 2400 1450 50  0000 L CNN
F 1 "C" H 2400 1250 50  0000 L CNN
	1    2350 1350
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 4F5C4C99
P 1550 1350
F 0 "C?" H 1600 1450 50  0000 L CNN
F 1 "C" H 1600 1250 50  0000 L CNN
	1    1550 1350
	1    0    0    -1  
$EndComp
$Comp
L 7805 U?
U 1 1 4F5C4BF3
P 1950 1200
F 0 "U?" H 2100 960 60  0000 C CNN
F 1 "AP1084" H 1955 1340 60  0000 C CNN
	1    1950 1200
	1    0    0    -1  
$EndComp
$EndSCHEMATC
