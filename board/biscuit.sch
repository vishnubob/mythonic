EESchema Schematic File Version 2  date 4/22/2012 5:14:17 PM
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
LIBS:shardy
LIBS:biscuit-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "22 apr 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L PWR_FLAG #FLG02
U 1 1 4F8933BA
P 10400 1300
F 0 "#FLG02" H 10400 1395 30  0001 C CNN
F 1 "PWR_FLAG" H 10400 1480 30  0000 C CNN
	1    10400 1300
	1    0    0    -1  
$EndComp
$Comp
L DGND #PWR03
U 1 1 4F893276
P 8850 1800
F 0 "#PWR03" H 8850 1800 40  0001 C CNN
F 1 "DGND" H 8850 1730 40  0000 C CNN
	1    8850 1800
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG04
U 1 1 4F893226
P 9800 1300
F 0 "#FLG04" H 9800 1395 30  0001 C CNN
F 1 "PWR_FLAG" H 9800 1480 30  0000 C CNN
	1    9800 1300
	1    0    0    -1  
$EndComp
$Comp
L DGND #PWR05
U 1 1 4F893219
P 10100 1550
F 0 "#PWR05" H 10100 1550 40  0001 C CNN
F 1 "DGND" H 10100 1480 40  0000 C CNN
	1    10100 1550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 4F8931E6
P 10400 1550
F 0 "#PWR06" H 10400 1550 30  0001 C CNN
F 1 "GND" H 10400 1480 30  0001 C CNN
	1    10400 1550
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR07
U 1 1 4F8931DD
P 9800 1550
F 0 "#PWR07" H 9800 1550 40  0001 C CNN
F 1 "GNDA" H 9800 1480 40  0000 C CNN
	1    9800 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	10100 1550 10100 1300
Wire Wire Line
	10400 1550 10400 1300
Wire Wire Line
	10400 1300 10200 1300
Wire Wire Line
	10000 1300 9800 1300
Wire Wire Line
	9800 1300 9800 1550
Wire Wire Line
	4150 5800 3800 5800
Wire Wire Line
	8100 6750 8250 6750
Wire Wire Line
	6300 6200 6650 6200
Wire Wire Line
	6500 6700 6650 6700
Wire Wire Line
	9850 5700 9850 5600
Wire Wire Line
	8250 5700 8250 5600
Wire Wire Line
	8250 5100 7900 5100
Wire Wire Line
	6500 5550 6650 5550
Wire Wire Line
	7200 3700 7200 3550
Wire Wire Line
	7200 3550 7600 3550
Wire Wire Line
	7850 3900 7700 3900
Wire Wire Line
	8900 2850 9250 2850
Wire Wire Line
	4150 6450 3800 6450
Wire Wire Line
	4150 6250 3800 6250
Wire Notes Line
	6800 800  6000 800 
Wire Notes Line
	6000 800  6000 650 
Wire Notes Line
	7600 2100 7600 2300
Wire Notes Line
	7600 2300 6900 2300
Wire Wire Line
	8900 4150 9250 4150
Wire Wire Line
	8900 3950 9250 3950
Wire Notes Line
	4800 3550 4200 3550
Wire Notes Line
	4200 3550 4200 3850
Wire Notes Line
	10400 4750 9700 4750
Wire Notes Line
	9700 4750 9700 4500
Wire Wire Line
	5800 6100 5800 5950
Wire Wire Line
	5800 5950 6300 5950
Connection ~ 6000 6700
Wire Wire Line
	6100 6700 5650 6700
Wire Wire Line
	5650 6700 5650 6600
Connection ~ 6650 6700
Wire Wire Line
	6300 6400 6300 6100
Wire Wire Line
	6300 6100 6200 6100
Wire Wire Line
	6000 6400 6000 6700
Connection ~ 6300 6200
Wire Wire Line
	6300 5800 5650 5800
Wire Wire Line
	5650 5800 5650 6100
Wire Wire Line
	7250 6150 7250 5850
Wire Wire Line
	7250 5850 7900 5850
Connection ~ 7900 6250
Wire Wire Line
	7600 6750 7600 6450
Wire Wire Line
	7800 6150 7900 6150
Wire Wire Line
	7900 6150 7900 6450
Connection ~ 8250 6750
Wire Wire Line
	7250 6650 7250 6750
Wire Wire Line
	7250 6750 7700 6750
Connection ~ 7600 6750
Wire Wire Line
	7900 6000 7400 6000
Wire Wire Line
	7400 6000 7400 6150
Wire Wire Line
	9000 6150 9000 6000
Wire Wire Line
	9000 6000 9500 6000
Connection ~ 9200 6750
Wire Wire Line
	9300 6750 8850 6750
Wire Wire Line
	8850 6750 8850 6650
Wire Wire Line
	10000 6850 10000 6500
Connection ~ 9850 6750
Wire Wire Line
	9500 6450 9500 6150
Wire Wire Line
	9500 6150 9400 6150
Wire Wire Line
	9200 6450 9200 6750
Connection ~ 10000 6750
Wire Wire Line
	9700 6750 10150 6750
Wire Wire Line
	10150 6250 9500 6250
Connection ~ 9500 6250
Connection ~ 9850 6250
Wire Wire Line
	9500 5850 8850 5850
Wire Wire Line
	8850 5850 8850 6150
Wire Wire Line
	8850 5000 8850 4700
Wire Wire Line
	8850 4700 9500 4700
Connection ~ 9500 5100
Wire Wire Line
	9200 5600 9200 5300
Wire Wire Line
	9400 5000 9500 5000
Wire Wire Line
	9500 5000 9500 5300
Connection ~ 9850 5600
Wire Wire Line
	8850 5500 8850 5600
Wire Wire Line
	8850 5600 9300 5600
Connection ~ 9200 5600
Wire Wire Line
	9500 4850 9000 4850
Wire Wire Line
	9000 4850 9000 5000
Wire Wire Line
	7400 5000 7400 4850
Wire Wire Line
	7400 4850 7900 4850
Connection ~ 7600 5600
Wire Wire Line
	7700 5600 7250 5600
Wire Wire Line
	7250 5600 7250 5500
Connection ~ 8250 5600
Wire Wire Line
	7900 5300 7900 5000
Wire Wire Line
	7900 5000 7800 5000
Wire Wire Line
	7600 5300 7600 5600
Connection ~ 7900 5100
Wire Wire Line
	7900 4700 7250 4700
Wire Wire Line
	7250 4700 7250 5000
Wire Wire Line
	5650 4950 5650 4650
Wire Wire Line
	5650 4650 6300 4650
Connection ~ 6300 5050
Wire Wire Line
	6000 5550 6000 5250
Wire Wire Line
	6200 4950 6300 4950
Wire Wire Line
	6300 4950 6300 5250
Connection ~ 6650 5550
Wire Wire Line
	5650 5450 5650 5550
Wire Wire Line
	5650 5550 6100 5550
Connection ~ 6000 5550
Wire Wire Line
	4150 4550 3800 4550
Wire Notes Line
	9550 1900 9550 2000
Wire Notes Line
	9550 2000 6900 2000
Wire Notes Line
	6900 2000 6900 650 
Connection ~ 7550 1400
Wire Wire Line
	7550 1400 7650 1400
Wire Wire Line
	7650 1400 7650 1100
Connection ~ 7650 1700
Connection ~ 8350 1700
Wire Wire Line
	7650 1700 9400 1700
Wire Wire Line
	7450 1300 7550 1300
Wire Wire Line
	7550 1300 7550 1650
Wire Wire Line
	7550 1650 7450 1650
Connection ~ 10150 3100
Connection ~ 10150 3300
Wire Wire Line
	10150 3200 10050 3200
Connection ~ 10150 3500
Wire Wire Line
	10150 3400 10050 3400
Wire Wire Line
	8900 3100 9250 3100
Wire Wire Line
	8900 3300 9250 3300
Wire Wire Line
	8900 3500 9250 3500
Wire Wire Line
	8200 2800 7950 2800
Wire Wire Line
	7950 2800 7950 2400
Wire Notes Line
	5300 5200 5300 4200
Wire Notes Line
	5300 4200 1450 4200
Wire Notes Line
	1450 7000 5300 7000
Wire Notes Line
	5300 7000 5300 5150
Wire Wire Line
	6300 2200 6300 2150
Wire Wire Line
	6300 2150 6050 2150
Connection ~ 6300 1800
Wire Wire Line
	6650 1800 6300 1800
Connection ~ 4400 4750
Wire Wire Line
	4400 4700 4400 4800
Wire Wire Line
	4400 4700 4750 4700
Wire Wire Line
	3800 4750 4400 4750
Connection ~ 1650 4450
Wire Wire Line
	1650 4550 1650 4450
Wire Wire Line
	4150 6050 3800 6050
Wire Wire Line
	4150 5600 3800 5600
Wire Wire Line
	4150 5400 3800 5400
Wire Wire Line
	4900 5650 4900 5550
Wire Wire Line
	4600 5250 4600 5150
Wire Wire Line
	4600 5150 3800 5150
Wire Wire Line
	1900 6750 1550 6750
Wire Wire Line
	1900 4750 1900 4450
Wire Wire Line
	4150 6350 3800 6350
Wire Wire Line
	4150 4950 3800 4950
Wire Wire Line
	4150 6550 3800 6550
Connection ~ 9400 1100
Wire Wire Line
	9400 900  9400 1300
Wire Wire Line
	8850 1400 8850 1800
Wire Wire Line
	8350 1300 8350 950 
Wire Wire Line
	8250 1100 8450 1100
Wire Wire Line
	7000 950  7000 1100
Wire Wire Line
	4650 850  4650 950 
Wire Wire Line
	4100 1650 4650 1650
Wire Wire Line
	2650 2050 2650 1850
Wire Wire Line
	2650 3650 2650 3450
Wire Wire Line
	2650 3450 2350 3450
Wire Wire Line
	2650 1850 2350 1850
Wire Wire Line
	9250 2500 8900 2500
Wire Wire Line
	4200 1100 4200 1000
Wire Wire Line
	4200 1000 4100 1000
Wire Wire Line
	3550 850  3550 1200
Connection ~ 2800 1650
Wire Wire Line
	2800 2950 2350 2950
Connection ~ 2900 1550
Wire Wire Line
	2900 2850 2350 2850
Wire Wire Line
	3000 1650 2800 1650
Wire Wire Line
	2350 1350 2800 1350
Wire Wire Line
	4650 2250 4650 2350
Wire Wire Line
	4100 1450 4400 1450
Wire Wire Line
	10150 2700 10150 2600
Wire Wire Line
	10150 2600 10050 2600
Wire Wire Line
	10050 2500 10300 2500
Wire Wire Line
	10050 2400 10150 2400
Wire Wire Line
	10150 2400 10150 2300
Wire Wire Line
	4100 1750 4400 1750
Wire Wire Line
	3550 3050 3750 3050
Wire Wire Line
	3750 3050 3750 3350
Wire Wire Line
	3750 3350 3600 3350
Wire Wire Line
	2350 1250 2900 1250
Wire Wire Line
	3000 1550 2900 1550
Connection ~ 2900 2850
Wire Wire Line
	2900 1250 2900 3050
Wire Wire Line
	2900 3050 3050 3050
Wire Wire Line
	2800 1350 2800 3350
Wire Wire Line
	2800 3350 3000 3350
Connection ~ 2800 2950
Wire Wire Line
	3700 1000 3550 1000
Connection ~ 3550 1000
Wire Wire Line
	9250 2400 8900 2400
Wire Wire Line
	9250 2600 8900 2600
Wire Wire Line
	2350 1950 2650 1950
Connection ~ 2650 1950
Wire Wire Line
	2350 3550 2650 3550
Connection ~ 2650 3550
Wire Wire Line
	2650 2550 2650 2650
Wire Wire Line
	7250 2500 7000 2500
Wire Wire Line
	8200 2600 7650 2600
Wire Wire Line
	8200 3000 7950 3000
Wire Wire Line
	8200 2700 7650 2700
Wire Wire Line
	8200 2500 7650 2500
Wire Wire Line
	4100 1550 4650 1550
Wire Wire Line
	4650 1650 4650 1750
Wire Wire Line
	4650 1550 4650 1450
Wire Wire Line
	7200 950  7200 1100
Connection ~ 7200 1100
Connection ~ 8350 1100
Connection ~ 8850 1700
Connection ~ 8600 1700
Wire Wire Line
	9250 1100 9400 1100
Wire Wire Line
	8600 1700 8600 1550
Wire Wire Line
	4150 6650 3800 6650
Wire Wire Line
	4150 4850 3800 4850
Wire Wire Line
	4150 5900 3800 5900
Wire Wire Line
	1900 4450 1550 4450
Wire Wire Line
	1900 6750 1900 6650
Wire Wire Line
	1550 6750 1550 6850
Wire Wire Line
	3800 5050 5200 5050
Wire Wire Line
	5200 5050 5200 5250
Wire Wire Line
	4150 5300 3800 5300
Wire Wire Line
	4150 5500 3800 5500
Wire Wire Line
	4150 5700 3800 5700
Wire Wire Line
	4150 6150 3800 6150
Wire Wire Line
	1650 5050 1650 4950
Wire Wire Line
	4400 4800 4750 4800
Wire Wire Line
	6100 1700 6300 1700
Wire Wire Line
	6300 1700 6300 1900
Wire Wire Line
	6300 1900 6100 1900
Wire Wire Line
	5600 1900 5050 1900
Connection ~ 5450 1900
Wire Wire Line
	5050 1700 5600 1700
Wire Wire Line
	5450 1900 5450 2150
Wire Wire Line
	5450 2150 5650 2150
Wire Wire Line
	5600 1350 5400 1350
Wire Wire Line
	5400 1350 5400 1100
Wire Wire Line
	5000 900  5550 900 
Connection ~ 5400 1100
Wire Wire Line
	5000 1100 5550 1100
Wire Wire Line
	6050 1100 6250 1100
Wire Wire Line
	6250 1100 6250 900 
Wire Wire Line
	6250 900  6050 900 
Wire Wire Line
	6600 1000 6250 1000
Connection ~ 6250 1000
Wire Wire Line
	6000 1350 6250 1350
Wire Wire Line
	6250 1350 6250 1400
Wire Wire Line
	6300 3000 6300 2950
Wire Wire Line
	6300 2950 6050 2950
Connection ~ 6300 2600
Wire Wire Line
	6650 2600 6300 2600
Wire Wire Line
	6100 2500 6300 2500
Wire Wire Line
	6300 2500 6300 2700
Wire Wire Line
	6300 2700 6100 2700
Wire Wire Line
	5600 2700 5050 2700
Connection ~ 5450 2700
Wire Wire Line
	5050 2500 5600 2500
Wire Wire Line
	5450 2700 5450 2950
Wire Wire Line
	5450 2950 5650 2950
Wire Wire Line
	5650 3750 5450 3750
Wire Wire Line
	5450 3750 5450 3500
Wire Wire Line
	5050 3300 5600 3300
Connection ~ 5450 3500
Wire Wire Line
	5050 3500 5600 3500
Wire Wire Line
	6100 3500 6300 3500
Wire Wire Line
	6300 3500 6300 3300
Wire Wire Line
	6300 3300 6100 3300
Wire Wire Line
	6650 3400 6300 3400
Connection ~ 6300 3400
Wire Wire Line
	6050 3750 6300 3750
Wire Wire Line
	6300 3750 6300 3800
Wire Notes Line
	4800 3850 4800 650 
Wire Notes Line
	4800 3850 1300 3850
Wire Notes Line
	1300 3850 1300 650 
Wire Notes Line
	1300 650  4800 650 
Wire Notes Line
	1500 7000 1300 7000
Wire Notes Line
	1300 7000 1300 4200
Wire Notes Line
	1300 4200 1500 4200
Wire Wire Line
	7950 3000 7950 3150
Wire Wire Line
	8900 3600 9250 3600
Wire Wire Line
	8900 3400 9250 3400
Wire Wire Line
	8900 3200 9250 3200
Wire Wire Line
	10050 3600 10150 3600
Wire Wire Line
	10150 3500 10050 3500
Wire Wire Line
	10150 3300 10050 3300
Connection ~ 10150 3400
Wire Wire Line
	10150 3100 10050 3100
Connection ~ 10150 3200
Wire Wire Line
	10150 3600 10150 3000
Wire Wire Line
	7000 1100 7850 1100
Connection ~ 7650 1100
Wire Wire Line
	7450 1500 7650 1500
Wire Wire Line
	7650 1500 7650 1850
Wire Wire Line
	7650 1850 7450 1850
Wire Notes Line
	6900 650  9550 650 
Wire Notes Line
	9550 650  9550 1950
Wire Wire Line
	4150 4650 3800 4650
Wire Wire Line
	6300 4800 5800 4800
Wire Wire Line
	5800 4800 5800 4950
Wire Notes Line
	5500 7000 5500 4500
Wire Notes Line
	5500 7000 10400 7000
Wire Notes Line
	10400 7000 10400 4500
Wire Notes Line
	10400 4500 5500 4500
Wire Notes Line
	4850 7000 4850 6700
Wire Notes Line
	4850 6700 5300 6700
Wire Wire Line
	8900 3850 9250 3850
Wire Wire Line
	8900 4050 9250 4050
Wire Notes Line
	6900 4400 10400 4400
Wire Notes Line
	6900 4400 6900 2100
Wire Notes Line
	6900 2100 10400 2100
Wire Notes Line
	10400 2100 10400 4400
Wire Notes Line
	4900 700  4900 4000
Wire Notes Line
	4900 4000 6800 4000
Wire Notes Line
	6800 4000 6800 650 
Wire Notes Line
	6800 650  4900 650 
Wire Notes Line
	4900 650  4900 750 
Wire Notes Line
	9100 2000 9100 1800
Wire Notes Line
	9100 1800 9550 1800
Wire Wire Line
	9750 2850 9950 2850
Wire Wire Line
	7850 3700 7700 3700
Wire Wire Line
	8700 4000 8700 3800
Wire Wire Line
	8700 3800 8500 3800
Wire Wire Line
	7600 4050 7200 4050
Wire Wire Line
	7200 4050 7200 3900
Wire Wire Line
	6300 5050 6650 5050
Wire Wire Line
	6650 5550 6650 5650
Wire Wire Line
	8250 5600 8100 5600
Wire Wire Line
	9850 5600 9700 5600
Wire Wire Line
	9850 5100 9500 5100
Wire Wire Line
	6650 6700 6650 6800
Wire Wire Line
	7900 6250 8250 6250
Wire Wire Line
	8250 6750 8250 6850
Wire Wire Line
	4150 6750 3800 6750
Wire Wire Line
	3550 2100 3550 2000
$Comp
L CONN_3 JP2
U 1 1 4F893179
P 10100 950
F 0 "JP2" V 10050 950 50  0000 C CNN
F 1 "CONN_3" V 10150 950 40  0000 C CNN
	1    10100 950 
	0    -1   -1   0   
$EndComp
$Comp
L GNDA #PWR08
U 1 1 4F8898ED
P 4200 1100
F 0 "#PWR08" H 4200 1100 40  0001 C CNN
F 1 "GNDA" H 4200 1030 40  0000 C CNN
	1    4200 1100
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P6
U 1 1 4F88959E
P 9600 4000
F 0 "P6" V 9550 4000 50  0000 C CNN
F 1 "CONN_4" V 9650 4000 50  0000 C CNN
	1    9600 4000
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR09
U 1 1 4F878BB5
P 3550 2100
F 0 "#PWR09" H 3550 2100 40  0001 C CNN
F 1 "GNDA" H 3550 2030 40  0000 C CNN
	1    3550 2100
	1    0    0    -1  
$EndComp
$Comp
L C C9
U 1 1 4F877813
P 9400 1500
F 0 "C9" H 9450 1600 50  0000 L CNN
F 1 ".1uF" H 9450 1400 50  0000 L CNN
	1    9400 1500
	-1   0    0    -1  
$EndComp
$Comp
L C C8
U 1 1 4F8777C0
P 8350 1500
F 0 "C8" H 8400 1600 50  0000 L CNN
F 1 ".33uF" H 8400 1400 50  0000 L CNN
	1    8350 1500
	1    0    0    -1  
$EndComp
Text Label 3850 6750 0    60   ~ 0
CTRLDE
Text Label 3850 5800 0    60   ~ 0
CTRLRE
$Comp
L GNDA #PWR010
U 1 1 4F7CB74E
P 4900 5650
F 0 "#PWR010" H 4900 5650 40  0001 C CNN
F 1 "GNDA" H 4900 5580 40  0000 C CNN
	1    4900 5650
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR011
U 1 1 4F7CB734
P 1650 5050
F 0 "#PWR011" H 1650 5050 40  0001 C CNN
F 1 "GNDA" H 1650 4980 40  0000 C CNN
	1    1650 5050
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR012
U 1 1 4F7CB71B
P 1550 6850
F 0 "#PWR012" H 1550 6850 40  0001 C CNN
F 1 "GNDA" H 1550 6780 40  0000 C CNN
	1    1550 6850
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR013
U 1 1 4F7CB6FD
P 4650 2350
F 0 "#PWR013" H 4650 2350 40  0001 C CNN
F 1 "GNDA" H 4650 2280 40  0000 C CNN
	1    4650 2350
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR014
U 1 1 4F7CB6EC
P 6300 3800
F 0 "#PWR014" H 6300 3800 40  0001 C CNN
F 1 "GNDA" H 6300 3730 40  0000 C CNN
	1    6300 3800
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR015
U 1 1 4F7CB6EA
P 6300 3000
F 0 "#PWR015" H 6300 3000 40  0001 C CNN
F 1 "GNDA" H 6300 2930 40  0000 C CNN
	1    6300 3000
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR016
U 1 1 4F7CB6E4
P 6300 2200
F 0 "#PWR016" H 6300 2200 40  0001 C CNN
F 1 "GNDA" H 6300 2130 40  0000 C CNN
	1    6300 2200
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR017
U 1 1 4F7CB6DF
P 6250 1400
F 0 "#PWR017" H 6250 1400 40  0001 C CNN
F 1 "GNDA" H 6250 1330 40  0000 C CNN
	1    6250 1400
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR018
U 1 1 4F7CB6B3
P 10150 2700
F 0 "#PWR018" H 10150 2700 40  0001 C CNN
F 1 "GNDA" H 10150 2630 40  0000 C CNN
	1    10150 2700
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR019
U 1 1 4F7CB6A9
P 7950 3150
F 0 "#PWR019" H 7950 3150 40  0001 C CNN
F 1 "GNDA" H 7950 3080 40  0000 C CNN
	1    7950 3150
	1    0    0    -1  
$EndComp
$Comp
L GNDA #PWR020
U 1 1 4F7CB660
P 8700 4000
F 0 "#PWR020" H 8700 4000 40  0001 C CNN
F 1 "GNDA" H 8700 3930 40  0000 C CNN
	1    8700 4000
	1    0    0    -1  
$EndComp
Text Label 7600 4050 2    60   ~ 0
GRN
Text Label 7600 3550 2    60   ~ 0
RED
$Comp
L R R19
U 1 1 4F7A7D9E
P 7450 3700
F 0 "R19" V 7530 3700 50  0000 C CNN
F 1 "150" V 7450 3700 50  0000 C CNN
	1    7450 3700
	0    -1   -1   0   
$EndComp
$Comp
L R R20
U 1 1 4F7A7D9A
P 7450 3900
F 0 "R20" V 7530 3900 50  0000 C CNN
F 1 "120" V 7450 3900 50  0000 C CNN
	1    7450 3900
	0    -1   -1   0   
$EndComp
$Comp
L BI_LED D2
U 1 1 4F7A7D70
P 8150 3800
F 0 "D2" H 8450 3900 50  0000 C CNN
F 1 "BI_LED" H 8500 3700 50  0000 C CNN
	1    8150 3800
	1    0    0    -1  
$EndComp
Text Label 4150 6450 2    60   ~ 0
GRN
Text Label 4150 6250 2    60   ~ 0
RED
Text Label 9500 1950 2    60   ~ 0
POWER
Text Label 6750 750  2    60   ~ 0
TOUCH DRIVERS
Text Label 7500 2250 2    60   ~ 0
INTERFACES
Text Label 9100 4150 2    60   ~ 0
TPN4
Text Label 9100 4050 2    60   ~ 0
TPN3
Text Label 9100 3950 2    60   ~ 0
TPN2
Text Label 9100 3850 2    60   ~ 0
TPN1
Text Label 4700 3750 2    60   ~ 0
RS-485
Text Label 5150 6900 2    60   ~ 0
MCU
Text Label 10350 4650 2    60   ~ 0
LED DRIVERS
$Comp
L GND #PWR021
U 1 1 4F78E4C7
P 6650 6800
F 0 "#PWR021" H 6650 6800 30  0001 C CNN
F 1 "GND" H 6650 6730 30  0001 C CNN
	1    6650 6800
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_P Q2
U 1 1 4F78E4C5
P 6000 6200
F 0 "Q2" V 5850 6400 60  0000 R CNN
F 1 "FET" V 5850 6150 60  0000 R CNN
	1    6000 6200
	0    -1   -1   0   
$EndComp
$Comp
L BC237 Q4
U 1 1 4F78E4C4
P 6300 6600
F 0 "Q4" V 6300 6800 50  0000 C CNN
F 1 "NPN" V 6300 6400 50  0000 C CNN
F 2 "TO92-EBC" H 6490 6600 30  0001 C CNN
	1    6300 6600
	0    -1   1    0   
$EndComp
$Comp
L R R6
U 1 1 4F78E4C3
P 5650 6350
F 0 "R6" V 5730 6350 50  0000 C CNN
F 1 "10K" V 5650 6350 50  0000 C CNN
	1    5650 6350
	1    0    0    -1  
$EndComp
$Comp
L R R16
U 1 1 4F78E4C2
P 6650 6450
F 0 "R16" V 6730 6450 50  0000 C CNN
F 1 "1.5 1W" V 6650 6450 50  0000 C CNN
	1    6650 6450
	1    0    0    1   
$EndComp
Text Label 6300 5950 2    60   ~ 0
LPN4
Text Label 6300 5800 2    60   ~ 0
LCH4
Text Label 7900 5850 2    60   ~ 0
LCH5
Text Label 7900 6000 2    60   ~ 0
LPN5
$Comp
L R R22
U 1 1 4F78E4C1
P 8250 6500
F 0 "R22" V 8330 6500 50  0000 C CNN
F 1 ".75 1W" V 8250 6500 50  0000 C CNN
	1    8250 6500
	1    0    0    1   
$EndComp
$Comp
L R R18
U 1 1 4F78E4C0
P 7250 6400
F 0 "R18" V 7330 6400 50  0000 C CNN
F 1 "10K" V 7250 6400 50  0000 C CNN
	1    7250 6400
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q8
U 1 1 4F78E4BF
P 7900 6650
F 0 "Q8" V 7900 6850 50  0000 C CNN
F 1 "NPN" V 7900 6450 50  0000 C CNN
F 2 "TO92-EBC" H 8090 6650 30  0001 C CNN
	1    7900 6650
	0    -1   1    0   
$EndComp
$Comp
L MOSFET_P Q6
U 1 1 4F78E4BE
P 7600 6250
F 0 "Q6" V 7450 6450 60  0000 R CNN
F 1 "FET" V 7450 6200 60  0000 R CNN
	1    7600 6250
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR022
U 1 1 4F78E4BC
P 8250 6850
F 0 "#PWR022" H 8250 6850 30  0001 C CNN
F 1 "GND" H 8250 6780 30  0001 C CNN
	1    8250 6850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR023
U 1 1 4F78E4BB
P 10000 6850
F 0 "#PWR023" H 10000 6850 30  0001 C CNN
F 1 "GND" H 10000 6780 30  0001 C CNN
	1    10000 6850
	1    0    0    -1  
$EndComp
$Comp
L POT RV6
U 1 1 4F78E4BA
P 10150 6500
F 0 "RV6" H 10150 6400 50  0000 C CNN
F 1 "10 1/2W" H 10150 6500 50  0000 C CNN
	1    10150 6500
	0    -1   1    0   
$EndComp
$Comp
L MOSFET_P Q10
U 1 1 4F78E4B9
P 9200 6250
F 0 "Q10" V 9050 6450 60  0000 R CNN
F 1 "FET" V 9050 6200 60  0000 R CNN
	1    9200 6250
	0    -1   -1   0   
$EndComp
$Comp
L BC237 Q12
U 1 1 4F78E4B8
P 9500 6650
F 0 "Q12" V 9500 6850 50  0000 C CNN
F 1 "NPN" V 9500 6450 50  0000 C CNN
F 2 "TO92-EBC" H 9690 6650 30  0001 C CNN
	1    9500 6650
	0    -1   1    0   
$EndComp
$Comp
L R R24
U 1 1 4F78E4B7
P 8850 6400
F 0 "R24" V 8930 6400 50  0000 C CNN
F 1 "10K" V 8850 6400 50  0000 C CNN
	1    8850 6400
	1    0    0    -1  
$EndComp
$Comp
L R R27
U 1 1 4F78E4B6
P 9850 6500
F 0 "R27" V 9930 6500 50  0000 C CNN
F 1 "2 1/2W" V 9850 6500 50  0000 C CNN
	1    9850 6500
	1    0    0    1   
$EndComp
Text Label 9500 6000 2    60   ~ 0
LPN2
Text Label 9500 5850 2    60   ~ 0
LCH2
Text Label 9500 4700 2    60   ~ 0
LCH3
Text Label 9500 4850 2    60   ~ 0
LPN3
$Comp
L R R26
U 1 1 4F78E49A
P 9850 5350
F 0 "R26" V 9930 5350 50  0000 C CNN
F 1 "1.5 1W" V 9850 5350 50  0000 C CNN
	1    9850 5350
	1    0    0    1   
$EndComp
$Comp
L R R23
U 1 1 4F78E499
P 8850 5250
F 0 "R23" V 8930 5250 50  0000 C CNN
F 1 "10K" V 8850 5250 50  0000 C CNN
	1    8850 5250
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q11
U 1 1 4F78E498
P 9500 5500
F 0 "Q11" V 9500 5700 50  0000 C CNN
F 1 "NPN" V 9500 5300 50  0000 C CNN
F 2 "TO92-EBC" H 9690 5500 30  0001 C CNN
	1    9500 5500
	0    -1   1    0   
$EndComp
$Comp
L MOSFET_P Q9
U 1 1 4F78E497
P 9200 5100
F 0 "Q9" V 9050 5300 60  0000 R CNN
F 1 "FET" V 9050 5050 60  0000 R CNN
	1    9200 5100
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR024
U 1 1 4F78E495
P 9850 5700
F 0 "#PWR024" H 9850 5700 30  0001 C CNN
F 1 "GND" H 9850 5630 30  0001 C CNN
	1    9850 5700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR025
U 1 1 4F78E483
P 8250 5700
F 0 "#PWR025" H 8250 5700 30  0001 C CNN
F 1 "GND" H 8250 5630 30  0001 C CNN
	1    8250 5700
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_P Q5
U 1 1 4F78E481
P 7600 5100
F 0 "Q5" V 7450 5300 60  0000 R CNN
F 1 "FET" V 7450 5050 60  0000 R CNN
	1    7600 5100
	0    -1   -1   0   
$EndComp
$Comp
L BC237 Q7
U 1 1 4F78E480
P 7900 5500
F 0 "Q7" V 7900 5700 50  0000 C CNN
F 1 "NPN" V 7900 5300 50  0000 C CNN
F 2 "TO92-EBC" H 8090 5500 30  0001 C CNN
	1    7900 5500
	0    -1   1    0   
$EndComp
$Comp
L R R17
U 1 1 4F78E47F
P 7250 5250
F 0 "R17" V 7330 5250 50  0000 C CNN
F 1 "10K" V 7250 5250 50  0000 C CNN
	1    7250 5250
	1    0    0    -1  
$EndComp
$Comp
L R R21
U 1 1 4F78E47E
P 8250 5350
F 0 "R21" V 8330 5350 50  0000 C CNN
F 1 "1.5 1W" V 8250 5350 50  0000 C CNN
	1    8250 5350
	1    0    0    1   
$EndComp
Text Label 7900 4850 2    60   ~ 0
LPN6
Text Label 7900 4700 2    60   ~ 0
LCH6
Text Label 6300 4650 2    60   ~ 0
LCH1
Text Label 6300 4800 2    60   ~ 0
LPN1
$Comp
L R R15
U 1 1 4F78E428
P 6650 5300
F 0 "R15" V 6730 5300 50  0000 C CNN
F 1 "1.3 1W" V 6650 5300 50  0000 C CNN
	1    6650 5300
	1    0    0    1   
$EndComp
$Comp
L R R5
U 1 1 4F78E427
P 5650 5200
F 0 "R5" V 5730 5200 50  0000 C CNN
F 1 "10K" V 5650 5200 50  0000 C CNN
	1    5650 5200
	1    0    0    -1  
$EndComp
$Comp
L BC237 Q3
U 1 1 4F78E426
P 6300 5450
F 0 "Q3" V 6300 5650 50  0000 C CNN
F 1 "NPN" V 6300 5250 50  0000 C CNN
F 2 "TO92-EBC" H 6490 5450 30  0001 C CNN
	1    6300 5450
	0    -1   1    0   
$EndComp
$Comp
L MOSFET_P Q1
U 1 1 4F78E425
P 6000 5050
F 0 "Q1" V 5850 5250 60  0000 R CNN
F 1 "FET" V 5850 5000 60  0000 R CNN
	1    6000 5050
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR026
U 1 1 4F78E423
P 6650 5650
F 0 "#PWR026" H 6650 5650 30  0001 C CNN
F 1 "GND" H 6650 5580 30  0001 C CNN
	1    6650 5650
	1    0    0    -1  
$EndComp
Text Label 4150 4650 2    60   ~ 0
LCH2
Text Label 4150 4550 2    60   ~ 0
LCH1
Text Label 4750 4800 2    60   ~ 0
LCH3
Text Label 4150 6650 2    60   ~ 0
LCH6
Text Label 4150 6550 2    60   ~ 0
LCH5
Text Label 4150 6350 2    60   ~ 0
LCH4
Text Label 8900 3600 0    60   ~ 0
LPN6
Text Label 8900 3500 0    60   ~ 0
LPN5
Text Label 8900 3400 0    60   ~ 0
LPN4
Text Label 8900 3300 0    60   ~ 0
LPN3
Text Label 8900 3200 0    60   ~ 0
LPN2
Text Label 8900 3100 0    60   ~ 0
LPN1
NoConn ~ 3800 4450
$Comp
L CONN_2 P2
U 1 1 4F780693
P 7100 1750
F 0 "P2" V 7050 1750 40  0000 C CNN
F 1 "PWR_OUT" V 7150 1750 40  0000 C CNN
	1    7100 1750
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P1
U 1 1 4F780686
P 7100 1400
F 0 "P1" V 7050 1400 40  0000 C CNN
F 1 "PWR_IN" V 7150 1400 40  0000 C CNN
	1    7100 1400
	-1   0    0    1   
$EndComp
NoConn ~ 2350 3250
NoConn ~ 2350 3150
NoConn ~ 2350 1650
NoConn ~ 2350 1550
$Comp
L +12V #PWR027
U 1 1 4F755945
P 10150 3000
F 0 "#PWR027" H 10150 2950 20  0001 C CNN
F 1 "+12V" H 10150 3100 30  0000 C CNN
	1    10150 3000
	1    0    0    -1  
$EndComp
$Comp
L CONN_6X2 P5
U 1 1 4F755840
P 9650 3350
F 0 "P5" H 9650 3700 60  0000 C CNN
F 1 "CONN_6X2" V 9650 3350 60  0000 C CNN
	1    9650 3350
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR028
U 1 1 4F754D87
P 7950 2400
F 0 "#PWR028" H 7950 2500 30  0001 C CNN
F 1 "VCC" H 7950 2500 30  0000 C CNN
	1    7950 2400
	1    0    0    -1  
$EndComp
$Comp
L R R13
U 1 1 4F754A43
P 5850 3300
F 0 "R13" V 5930 3300 50  0000 C CNN
F 1 "10M" V 5850 3300 50  0000 C CNN
	1    5850 3300
	0    -1   -1   0   
$EndComp
$Comp
L R R14
U 1 1 4F754A42
P 5850 3500
F 0 "R14" V 5930 3500 50  0000 C CNN
F 1 "10K" V 5850 3500 50  0000 C CNN
	1    5850 3500
	0    -1   -1   0   
$EndComp
$Comp
L C C6
U 1 1 4F754A41
P 5850 3750
F 0 "C6" V 5950 3800 50  0000 L CNN
F 1 "100pF" V 5950 3500 50  0000 L CNN
	1    5850 3750
	0    1    1    0   
$EndComp
Text Label 5050 3300 0    60   ~ 0
CHRG
Text Label 5050 3500 0    60   ~ 0
TCH4
Text Label 6450 3400 0    60   ~ 0
TPN4
Text Label 6450 2600 0    60   ~ 0
TPN3
Text Label 5050 2700 0    60   ~ 0
TCH3
Text Label 5050 2500 0    60   ~ 0
CHRG
$Comp
L C C5
U 1 1 4F754A3E
P 5850 2950
F 0 "C5" V 5950 3000 50  0000 L CNN
F 1 "100pF" V 5950 2700 50  0000 L CNN
	1    5850 2950
	0    1    1    0   
$EndComp
$Comp
L R R12
U 1 1 4F754A3D
P 5850 2700
F 0 "R12" V 5930 2700 50  0000 C CNN
F 1 "10K" V 5850 2700 50  0000 C CNN
	1    5850 2700
	0    -1   -1   0   
$EndComp
$Comp
L R R11
U 1 1 4F754A3C
P 5850 2500
F 0 "R11" V 5930 2500 50  0000 C CNN
F 1 "10M" V 5850 2500 50  0000 C CNN
	1    5850 2500
	0    -1   -1   0   
$EndComp
$Comp
L R R7
U 1 1 4F754A36
P 5800 900
F 0 "R7" V 5880 900 50  0000 C CNN
F 1 "10M" V 5800 900 50  0000 C CNN
	1    5800 900 
	0    -1   -1   0   
$EndComp
$Comp
L R R8
U 1 1 4F754A35
P 5800 1100
F 0 "R8" V 5880 1100 50  0000 C CNN
F 1 "10K" V 5800 1100 50  0000 C CNN
	1    5800 1100
	0    -1   -1   0   
$EndComp
$Comp
L C C3
U 1 1 4F754A34
P 5800 1350
F 0 "C3" V 5900 1400 50  0000 L CNN
F 1 "100pF" V 5900 1100 50  0000 L CNN
	1    5800 1350
	0    1    1    0   
$EndComp
Text Label 5000 900  0    60   ~ 0
CHRG
Text Label 5000 1100 0    60   ~ 0
TCH1
Text Label 6400 1000 0    60   ~ 0
TPN1
Text Label 6450 1800 0    60   ~ 0
TPN2
Text Label 5050 1900 0    60   ~ 0
TCH2
Text Label 5050 1700 0    60   ~ 0
CHRG
$Comp
L C C4
U 1 1 4F754716
P 5850 2150
F 0 "C4" V 5950 2200 50  0000 L CNN
F 1 "100pF" V 5950 1900 50  0000 L CNN
	1    5850 2150
	0    1    1    0   
$EndComp
$Comp
L R R10
U 1 1 4F7546DA
P 5850 1900
F 0 "R10" V 5930 1900 50  0000 C CNN
F 1 "10K" V 5850 1900 50  0000 C CNN
	1    5850 1900
	0    -1   -1   0   
$EndComp
$Comp
L R R9
U 1 1 4F7546B5
P 5850 1700
F 0 "R9" V 5930 1700 50  0000 C CNN
F 1 "10M" V 5850 1700 50  0000 C CNN
	1    5850 1700
	0    -1   -1   0   
$EndComp
Text Label 4550 4700 0    60   ~ 0
MOSI
NoConn ~ 1900 5050
$Comp
L C C1
U 1 1 4F75425C
P 1650 4750
F 0 "C1" H 1700 4850 50  0000 L CNN
F 1 "0.1uF" H 1700 4650 50  0000 L CNN
	1    1650 4750
	-1   0    0    1   
$EndComp
Text Label 4000 6150 0    60   ~ 0
TXD
Text Label 4000 6050 0    60   ~ 0
RXD
Text Label 3950 5700 0    60   ~ 0
TCH4
Text Label 3950 5600 0    60   ~ 0
TCH3
Text Label 3950 5500 0    60   ~ 0
TCH2
Text Label 3950 5400 0    60   ~ 0
TCH1
Text Label 3950 5300 0    60   ~ 0
CHRG
Text Label 8900 2850 0    60   ~ 0
RESET
$Comp
L VCC #PWR029
U 1 1 4F753070
P 9950 2850
F 0 "#PWR029" H 9950 2950 30  0001 C CNN
F 1 "VCC" H 9950 2950 30  0000 C CNN
	1    9950 2850
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR030
U 1 1 4F752E45
P 1550 4450
F 0 "#PWR030" H 1550 4550 30  0001 C CNN
F 1 "VCC" H 1550 4550 30  0000 C CNN
	1    1550 4450
	1    0    0    -1  
$EndComp
Text Label 3900 5900 0    60   ~ 0
RESET
Text Label 4000 4950 0    60   ~ 0
SCK
Text Label 3950 4850 0    60   ~ 0
MISO
$Comp
L RESONATOR Y1
U 1 1 4F7524F4
P 4900 5300
F 0 "Y1" H 5000 5100 60  0000 C CNN
F 1 "RESONATOR" H 4900 5600 60  0000 C CNN
	1    4900 5300
	1    0    0    -1  
$EndComp
$Comp
L ATMEGA328-P IC1
U 1 1 4F7521F9
P 2800 5550
F 0 "IC1" H 2100 6800 50  0000 L BNN
F 1 "ATMEGA328-P" H 3050 4150 50  0000 L BNN
F 2 "DIL28" H 2200 4200 50  0001 C CNN
	1    2800 5550
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG031
U 1 1 4F74F9B9
P 8600 1550
F 0 "#FLG031" H 8600 1820 30  0001 C CNN
F 1 "PWR_FLAG" H 8600 1780 30  0000 C CNN
	1    8600 1550
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG032
U 1 1 4F74F9B6
P 8350 950
F 0 "#FLG032" H 8350 1220 30  0001 C CNN
F 1 "PWR_FLAG" H 8350 1180 30  0000 C CNN
	1    8350 950 
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG033
U 1 1 4F74F98C
P 7200 950
F 0 "#FLG033" H 7200 1220 30  0001 C CNN
F 1 "PWR_FLAG" H 7200 1180 30  0000 C CNN
	1    7200 950 
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR034
U 1 1 4F74EFBE
P 9400 900
F 0 "#PWR034" H 9400 1000 30  0001 C CNN
F 1 "VCC" H 9400 1000 30  0000 C CNN
	1    9400 900 
	1    0    0    -1  
$EndComp
$Comp
L +12V #PWR035
U 1 1 4F74EF00
P 7000 950
F 0 "#PWR035" H 7000 900 20  0001 C CNN
F 1 "+12V" H 7000 1050 30  0000 C CNN
	1    7000 950 
	1    0    0    -1  
$EndComp
$Comp
L DIODE D1
U 1 1 4F74EEA7
P 8050 1100
F 0 "D1" H 8050 1200 40  0000 C CNN
F 1 "1N4004" H 8050 1000 40  0000 C CNN
	1    8050 1100
	1    0    0    -1  
$EndComp
$Comp
L CONN_3X2 P4
U 1 1 4F74EC9E
P 9650 2550
F 0 "P4" H 9650 2800 50  0000 C CNN
F 1 "ICSP" V 9650 2600 40  0000 C CNN
	1    9650 2550
	1    0    0    -1  
$EndComp
Text Label 8900 2400 0    60   ~ 0
MISO
Text Label 8900 2500 0    60   ~ 0
SCK
Text Label 8900 2600 0    60   ~ 0
RESET
Text Label 10100 2500 0    60   ~ 0
MOSI
$Comp
L VCC #PWR036
U 1 1 4F74EC9D
P 10150 2300
F 0 "#PWR036" H 10150 2400 30  0001 C CNN
F 1 "VCC" H 10150 2400 30  0000 C CNN
	1    10150 2300
	1    0    0    -1  
$EndComp
$Comp
L MAX485 U1
U 1 1 4F74EC9B
P 3550 1600
F 0 "U1" H 3350 1900 60  0000 C CNN
F 1 "MAX485" H 3750 1300 60  0000 C CNN
	1    3550 1600
	-1   0    0    -1  
$EndComp
Text Label 4100 1450 0    60   ~ 0
RXD
Text Label 4100 1750 0    60   ~ 0
TXD
Text Label 4100 1550 0    60   ~ 0
CTRLRE
$Comp
L VCC #PWR037
U 1 1 4F74EC9A
P 3550 850
F 0 "#PWR037" H 3550 950 30  0001 C CNN
F 1 "VCC" H 3550 950 30  0000 C CNN
	1    3550 850 
	1    0    0    -1  
$EndComp
$Comp
L JUMPER JP1
U 1 1 4F74EC98
P 3300 3350
F 0 "JP1" H 3300 3500 60  0000 C CNN
F 1 "JUMPER" H 3300 3270 40  0000 C CNN
	1    3300 3350
	-1   0    0    1   
$EndComp
$Comp
L R R2
U 1 1 4F74EC97
P 3300 3050
F 0 "R2" V 3380 3050 50  0000 C CNN
F 1 "120" V 3300 3050 50  0000 C CNN
	1    3300 3050
	0    -1   -1   0   
$EndComp
$Comp
L R R1
U 1 1 4F74EC96
P 2650 2300
F 0 "R1" V 2730 2300 50  0000 C CNN
F 1 "100 1/2W" V 2550 2300 50  0000 C CNN
	1    2650 2300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR038
U 1 1 4F74EC95
P 2650 2650
F 0 "#PWR038" H 2650 2650 30  0001 C CNN
F 1 "GND" H 2650 2580 30  0001 C CNN
	1    2650 2650
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 4F74EC94
P 4650 2000
F 0 "R4" V 4730 2000 50  0000 C CNN
F 1 "10k" V 4650 2000 50  0000 C CNN
	1    4650 2000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR039
U 1 1 4F74EC92
P 2650 3650
F 0 "#PWR039" H 2650 3650 30  0001 C CNN
F 1 "GND" H 2650 3580 30  0001 C CNN
	1    2650 3650
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 4F74EC8E
P 3900 1000
F 0 "C2" H 3950 1100 50  0000 L CNN
F 1 "0.1uF" H 3950 900 50  0000 L CNN
	1    3900 1000
	0    -1   -1   0   
$EndComp
$Comp
L RJ45 J1
U 1 1 4F74EC8C
P 1900 1600
F 0 "J1" H 2100 2100 60  0000 C CNN
F 1 "IN" H 1750 2100 60  0000 C CNN
	1    1900 1600
	0    -1   1    0   
$EndComp
$Comp
L RJ45 J2
U 1 1 4F74EC8B
P 1900 3200
F 0 "J2" H 2100 3700 60  0000 C CNN
F 1 "OUT" H 1750 3700 60  0000 C CNN
	1    1900 3200
	0    -1   1    0   
$EndComp
NoConn ~ 2350 1450
NoConn ~ 2350 1750
NoConn ~ 2350 3050
NoConn ~ 2350 3350
NoConn ~ 1550 2150
NoConn ~ 1550 3750
NoConn ~ 8200 2900
$Comp
L C C7
U 1 1 4F74EC87
P 7450 2500
F 0 "C7" H 7500 2600 50  0000 L CNN
F 1 "0.1uF" H 7500 2400 50  0000 L CNN
	1    7450 2500
	0    1    1    0   
$EndComp
Text Label 7000 2500 0    60   ~ 0
RESET
Text Label 7650 2600 0    60   ~ 0
TXD
Text Label 7650 2700 0    60   ~ 0
RXD
$Comp
L CONN_6 P3
U 1 1 4F74EC84
P 8550 2750
F 0 "P3" V 8500 2750 60  0000 C CNN
F 1 "TTL-232R" V 8600 2750 60  0000 C CNN
	1    8550 2750
	1    0    0    1   
$EndComp
Text Label 4100 1650 0    60   ~ 0
CTRLDE
$Comp
L R R3
U 1 1 4F74EC83
P 4650 1200
F 0 "R3" V 4730 1200 50  0000 C CNN
F 1 "10k" V 4650 1200 50  0000 C CNN
	1    4650 1200
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR040
U 1 1 4F74EC82
P 4650 850
F 0 "#PWR040" H 4650 950 30  0001 C CNN
F 1 "VCC" H 4650 950 30  0000 C CNN
	1    4650 850 
	1    0    0    -1  
$EndComp
$Comp
L R R25
U 1 1 4F6FF538
P 9500 2850
F 0 "R25" V 9580 2850 50  0000 C CNN
F 1 "10K" V 9500 2850 50  0000 C CNN
	1    9500 2850
	0    -1   -1   0   
$EndComp
$Comp
L 7805 U2
U 1 1 4F5C4BF3
P 8850 1150
F 0 "U2" H 9000 910 60  0000 C CNN
F 1 "7805" H 8850 1350 60  0000 C CNN
	1    8850 1150
	1    0    0    -1  
$EndComp
$EndSCHEMATC
