EESchema Schematic File Version 2  date 4/6/2012 3:41:14 AM
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
LIBS:giblib
LIBS:biscuit-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title "noname.sch"
Date "6 apr 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
NoConn ~ 5750 5400
Wire Wire Line
	7550 4700 7550 4800
Wire Wire Line
	7550 4800 7150 4800
Wire Wire Line
	7150 4700 7350 4700
Wire Wire Line
	7350 5000 7150 5000
Wire Wire Line
	7150 5100 7550 5100
Wire Wire Line
	7550 5100 7550 5200
$Comp
L GND #PWR?
U 1 1 4F7E9DA0
P 7550 5200
F 0 "#PWR?" H 7550 5200 30  0001 C CNN
F 1 "GND" H 7550 5130 30  0001 C CNN
	1    7550 5200
	1    0    0    -1  
$EndComp
Text Label 7200 5000 0    60   ~ 0
CLK
Text Label 7200 4700 0    60   ~ 0
LCH
$Comp
L VCC #PWR?
U 1 1 4F7E9D9F
P 7550 4700
F 0 "#PWR?" H 7550 4800 30  0001 C CNN
F 1 "VCC" H 7550 4800 30  0000 C CNN
	1    7550 4700
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR?
U 1 1 4F7E9D89
P 7550 3350
F 0 "#PWR?" H 7550 3450 30  0001 C CNN
F 1 "VCC" H 7550 3450 30  0000 C CNN
	1    7550 3350
	1    0    0    -1  
$EndComp
Text Label 7200 3350 0    60   ~ 0
LCH
Text Label 7200 3650 0    60   ~ 0
CLK
$Comp
L GND #PWR?
U 1 1 4F7E9D88
P 7550 3850
F 0 "#PWR?" H 7550 3850 30  0001 C CNN
F 1 "GND" H 7550 3780 30  0001 C CNN
	1    7550 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7550 3750 7550 3850
Wire Wire Line
	7150 3750 7550 3750
Wire Wire Line
	7350 3650 7150 3650
Wire Wire Line
	7150 3350 7350 3350
Wire Wire Line
	7550 3450 7150 3450
Wire Wire Line
	7550 3350 7550 3450
Wire Wire Line
	7150 3150 7150 2900
Wire Wire Line
	7150 2900 5750 2900
Wire Wire Line
	5750 2900 5750 2700
Wire Wire Line
	7550 2000 7550 2100
Wire Wire Line
	7550 2100 7150 2100
Wire Wire Line
	7150 2000 7350 2000
Wire Wire Line
	2200 1300 2000 1300
Wire Wire Line
	2200 900  2000 900 
Wire Wire Line
	5000 2400 5200 2400
Wire Wire Line
	5000 2200 5200 2200
Wire Wire Line
	5000 2000 5200 2000
Wire Wire Line
	5000 1800 5200 1800
Wire Wire Line
	5600 2500 5750 2500
Wire Wire Line
	5600 2300 5750 2300
Wire Wire Line
	5600 2100 5750 2100
Wire Wire Line
	5600 1900 5750 1900
Wire Wire Line
	5600 1800 5750 1800
Wire Wire Line
	5600 2000 5750 2000
Wire Wire Line
	5600 2200 5750 2200
Wire Wire Line
	5600 2400 5750 2400
Wire Wire Line
	5000 1900 5200 1900
Wire Wire Line
	5000 2100 5200 2100
Wire Wire Line
	5000 2300 5200 2300
Wire Wire Line
	5000 2500 5200 2500
Wire Wire Line
	5000 3850 5200 3850
Wire Wire Line
	5000 3650 5200 3650
Wire Wire Line
	5000 3450 5200 3450
Wire Wire Line
	5000 3250 5200 3250
Wire Wire Line
	5600 3750 5750 3750
Wire Wire Line
	5600 3550 5750 3550
Wire Wire Line
	5600 3350 5750 3350
Wire Wire Line
	5600 3150 5750 3150
Wire Wire Line
	5600 3250 5750 3250
Wire Wire Line
	5600 3450 5750 3450
Wire Wire Line
	5600 3650 5750 3650
Wire Wire Line
	5600 3850 5750 3850
Wire Wire Line
	5000 3150 5200 3150
Wire Wire Line
	5000 3350 5200 3350
Wire Wire Line
	5000 3550 5200 3550
Wire Wire Line
	5000 3750 5200 3750
Wire Wire Line
	5000 5100 5200 5100
Wire Wire Line
	5000 4900 5200 4900
Wire Wire Line
	5000 4700 5200 4700
Wire Wire Line
	5000 4500 5200 4500
Wire Wire Line
	5600 5200 5750 5200
Wire Wire Line
	5600 5000 5750 5000
Wire Wire Line
	5600 4800 5750 4800
Wire Wire Line
	5600 4600 5750 4600
Wire Wire Line
	5600 4500 5750 4500
Wire Wire Line
	5600 4700 5750 4700
Wire Wire Line
	5600 4900 5750 4900
Wire Wire Line
	5600 5100 5750 5100
Wire Wire Line
	5000 4600 5200 4600
Wire Wire Line
	5000 4800 5200 4800
Wire Wire Line
	5000 5000 5200 5000
Wire Wire Line
	5000 5200 5200 5200
Wire Wire Line
	2200 1100 2000 1100
Wire Wire Line
	850  1100 1100 1100
Wire Wire Line
	850  1850 1100 1850
Wire Wire Line
	2200 1850 2000 1850
Wire Wire Line
	2200 1650 2000 1650
Wire Wire Line
	2200 2050 2000 2050
Wire Wire Line
	2200 3500 2000 3500
Wire Wire Line
	2200 3100 2000 3100
Wire Wire Line
	2200 3300 2000 3300
Wire Wire Line
	850  3300 1100 3300
Wire Wire Line
	850  2550 1100 2550
Wire Wire Line
	2200 2550 2000 2550
Wire Wire Line
	2200 2350 2000 2350
Wire Wire Line
	2200 2750 2000 2750
Wire Wire Line
	2200 5700 2000 5700
Wire Wire Line
	2200 5300 2000 5300
Wire Wire Line
	2200 5500 2000 5500
Wire Wire Line
	850  5500 1100 5500
Wire Wire Line
	850  6250 1100 6250
Wire Wire Line
	2200 6250 2000 6250
Wire Wire Line
	2200 6050 2000 6050
Wire Wire Line
	2200 6450 2000 6450
Wire Wire Line
	2200 5000 2000 5000
Wire Wire Line
	2200 4600 2000 4600
Wire Wire Line
	2200 4800 2000 4800
Wire Wire Line
	850  4800 1100 4800
Wire Wire Line
	850  4050 1100 4050
Wire Wire Line
	2200 4050 2000 4050
Wire Wire Line
	2200 3850 2000 3850
Wire Wire Line
	2200 4250 2000 4250
Wire Wire Line
	7150 1800 7350 1800
Wire Wire Line
	7350 2300 7150 2300
Wire Wire Line
	9100 1400 9300 1400
Wire Wire Line
	9300 1900 9300 1800
Wire Wire Line
	7150 2400 7550 2400
Wire Wire Line
	7550 2400 7550 2500
Wire Wire Line
	5750 4050 5750 4250
Wire Wire Line
	5750 4250 7150 4250
Wire Wire Line
	7150 4250 7150 4500
$Comp
L GND #PWR?
U 1 1 4F7E9CE4
P 7550 2500
F 0 "#PWR?" H 7550 2500 30  0001 C CNN
F 1 "GND" H 7550 2430 30  0001 C CNN
	1    7550 2500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 4F7E9CB4
P 9300 1900
F 0 "#PWR?" H 9300 1900 30  0001 C CNN
F 1 "GND" H 9300 1830 30  0001 C CNN
	1    9300 1900
	1    0    0    -1  
$EndComp
Text Label 9100 1400 0    60   ~ 0
LCH
$Comp
L C C?
U 1 1 4F7E9BD4
P 9300 1600
F 0 "C?" H 9350 1700 50  0000 L CNN
F 1 "C" H 9350 1500 50  0000 L CNN
	1    9300 1600
	-1   0    0    1   
$EndComp
Text Label 7200 2300 0    60   ~ 0
CLK
Text Label 7200 2000 0    60   ~ 0
LCH
Text Label 7150 1800 0    60   ~ 0
DATA
$Comp
L VCC #PWR?
U 1 1 4F7E9AFB
P 7550 2000
F 0 "#PWR?" H 7550 2100 30  0001 C CNN
F 1 "VCC" H 7550 2100 30  0000 C CNN
	1    7550 2000
	1    0    0    -1  
$EndComp
$Comp
L TRI_LED D?
U 1 1 4F7E9952
P 1550 4050
F 0 "D?" H 1550 4370 50  0000 C CNN
F 1 "TRI_LED" H 1560 3720 50  0000 C CNN
	1    1550 4050
	-1   0    0    -1  
$EndComp
Text Label 2100 3850 0    60   ~ 0
R5
Text Label 2100 4050 0    60   ~ 0
G5
Text Label 2100 4250 0    60   ~ 0
B5
Text Label 850  4050 0    60   ~ 0
LC
Text Label 850  4800 0    60   ~ 0
LC
Text Label 2100 5000 0    60   ~ 0
B6
Text Label 2100 4800 0    60   ~ 0
G6
Text Label 2100 4600 0    60   ~ 0
R6
$Comp
L TRI_LED D?
U 1 1 4F7E9951
P 1550 4800
F 0 "D?" H 1550 5120 50  0000 C CNN
F 1 "TRI_LED" H 1560 4470 50  0000 C CNN
	1    1550 4800
	-1   0    0    -1  
$EndComp
$Comp
L TRI_LED D?
U 1 1 4F7E9950
P 1550 6250
F 0 "D?" H 1550 6570 50  0000 C CNN
F 1 "TRI_LED" H 1560 5920 50  0000 C CNN
	1    1550 6250
	-1   0    0    -1  
$EndComp
Text Label 2100 6050 0    60   ~ 0
R8
Text Label 2100 6250 0    60   ~ 0
G8
Text Label 2100 6450 0    60   ~ 0
B8
Text Label 850  6250 0    60   ~ 0
LC
Text Label 850  5500 0    60   ~ 0
LC
Text Label 2100 5700 0    60   ~ 0
B7
Text Label 2100 5500 0    60   ~ 0
G7
Text Label 2100 5300 0    60   ~ 0
R7
$Comp
L TRI_LED D?
U 1 1 4F7E994F
P 1550 5500
F 0 "D?" H 1550 5820 50  0000 C CNN
F 1 "TRI_LED" H 1560 5170 50  0000 C CNN
	1    1550 5500
	-1   0    0    -1  
$EndComp
$Comp
L TRI_LED D?
U 1 1 4F7E9937
P 1550 2550
F 0 "D?" H 1550 2870 50  0000 C CNN
F 1 "TRI_LED" H 1560 2220 50  0000 C CNN
	1    1550 2550
	-1   0    0    -1  
$EndComp
Text Label 2100 2350 0    60   ~ 0
R3
Text Label 2100 2550 0    60   ~ 0
G3
Text Label 2100 2750 0    60   ~ 0
B3
Text Label 850  2550 0    60   ~ 0
LC
Text Label 850  3300 0    60   ~ 0
LC
Text Label 2100 3500 0    60   ~ 0
B4
Text Label 2100 3300 0    60   ~ 0
G4
Text Label 2100 3100 0    60   ~ 0
R4
$Comp
L TRI_LED D?
U 1 1 4F7E9936
P 1550 3300
F 0 "D?" H 1550 3620 50  0000 C CNN
F 1 "TRI_LED" H 1560 2970 50  0000 C CNN
	1    1550 3300
	-1   0    0    -1  
$EndComp
$Comp
L TRI_LED D?
U 1 1 4F7E9916
P 1550 1850
F 0 "D?" H 1550 2170 50  0000 C CNN
F 1 "TRI_LED" H 1560 1520 50  0000 C CNN
	1    1550 1850
	-1   0    0    -1  
$EndComp
Text Label 2100 1650 0    60   ~ 0
R2
Text Label 2100 1850 0    60   ~ 0
G2
Text Label 2100 2050 0    60   ~ 0
B2
Text Label 850  1850 0    60   ~ 0
LC
Text Label 850  1100 0    60   ~ 0
LC
Text Label 2100 1300 0    60   ~ 0
B1
Text Label 2100 1100 0    60   ~ 0
G1
Text Label 2100 900  0    60   ~ 0
R1
Text Label 5000 5200 0    60   ~ 0
R8
Text Label 5000 5100 0    60   ~ 0
R7
Text Label 5000 5000 0    60   ~ 0
R6
Text Label 5000 4900 0    60   ~ 0
R5
Text Label 5000 4800 0    60   ~ 0
R4
Text Label 5000 4700 0    60   ~ 0
R3
Text Label 5000 4600 0    60   ~ 0
R2
Text Label 5000 4500 0    60   ~ 0
R1
$Comp
L R_PACK8 RP?
U 1 1 4F7E97EC
P 5400 4850
F 0 "RP?" H 5400 5300 40  0000 C CNN
F 1 "R_PACK8" H 5400 4400 40  0000 C CNN
	1    5400 4850
	1    0    0    -1  
$EndComp
$Comp
L 74HC595 U?
U 1 1 4F7E97EB
P 6450 4950
F 0 "U?" H 6600 5550 70  0000 C CNN
F 1 "74HC595" H 6450 4350 70  0000 C CNN
	1    6450 4950
	-1   0    0    -1  
$EndComp
$Comp
L 74HC595 U?
U 1 1 4F7E97E7
P 6450 3600
F 0 "U?" H 6600 4200 70  0000 C CNN
F 1 "74HC595" H 6450 3000 70  0000 C CNN
	1    6450 3600
	-1   0    0    -1  
$EndComp
$Comp
L R_PACK8 RP?
U 1 1 4F7E97E6
P 5400 3500
F 0 "RP?" H 5400 3950 40  0000 C CNN
F 1 "R_PACK8" H 5400 3050 40  0000 C CNN
	1    5400 3500
	1    0    0    -1  
$EndComp
Text Label 5000 3150 0    60   ~ 0
B1
Text Label 5000 3250 0    60   ~ 0
B2
Text Label 5000 3350 0    60   ~ 0
B3
Text Label 5000 3450 0    60   ~ 0
B4
Text Label 5000 3550 0    60   ~ 0
B5
Text Label 5000 3650 0    60   ~ 0
B6
Text Label 5000 3750 0    60   ~ 0
B7
Text Label 5000 3850 0    60   ~ 0
B8
Text Label 5000 2500 0    60   ~ 0
G8
Text Label 5000 2400 0    60   ~ 0
G7
Text Label 5000 2300 0    60   ~ 0
G6
Text Label 5000 2200 0    60   ~ 0
G5
Text Label 5000 2100 0    60   ~ 0
G4
Text Label 5000 2000 0    60   ~ 0
G3
Text Label 5000 1900 0    60   ~ 0
G2
Text Label 5000 1800 0    60   ~ 0
G1
$Comp
L R_PACK8 RP?
U 1 1 4F7E968C
P 5400 2150
F 0 "RP?" H 5400 2600 40  0000 C CNN
F 1 "R_PACK8" H 5400 1700 40  0000 C CNN
	1    5400 2150
	1    0    0    -1  
$EndComp
$Comp
L 74HC595 U?
U 1 1 4F7E961A
P 6450 2250
F 0 "U?" H 6600 2850 70  0000 C CNN
F 1 "74HC595" H 6450 1650 70  0000 C CNN
	1    6450 2250
	-1   0    0    -1  
$EndComp
$Comp
L TRI_LED D?
U 1 1 4F7E9327
P 1550 1100
F 0 "D?" H 1550 1420 50  0000 C CNN
F 1 "TRI_LED" H 1560 770 50  0000 C CNN
	1    1550 1100
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
