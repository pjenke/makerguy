State 0: Forwards -> 1000Ω, 5600Ω (0,15)
State 1: Left -> 3300Ω, 10000Ω (0,25)
State 2: Right -> 3900Ω, 7500Ω (0,34)
State 3: Program 1 -> 8200Ω, 10000Ω (0,45)
State 4: unused -> 10000Ω, 8200Ω (0,55)
State 5: unused -> 7500Ω, 3900Ω (0,66)
State 6: unused -> 10000Ω, 3300Ω (0,75)
State 7: unused -> 5600Ω, 1000Ω (0,85)


    - - 
  /  0 |
 | 2 1 | 
  - - -

0: GND
1: DATA
2: 5V
0 -> 1: R1
0 -> 2: R2


*** Terminal connection to ESP8266 ***
Commands (
Reference: https://room-15.github.io/blog/2015/03/26/esp8266-at-command-reference/#AT+GMR
Heise Developer: https://www.heise.de/developer/artikel/Arduino-goes-ESP8266-3240085.html
- AT -> OK
- AT+CWMODE=1 (Client Mode)
- AT+CWLAP (List all access points)
- AT+CWJAP_DEF=„SSID“,“PASSWORD“ (connect to Wifi)