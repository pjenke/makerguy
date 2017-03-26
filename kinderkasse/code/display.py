#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of ToyRegister.
# 
# ToyRegister is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ToyRegister is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ToyRegister.  If not, see <http://www.gnu.org/licenses/>.
# 
# Diese Datei ist Teil von ToyRegister.
# 
# ToyRegister ist Freie Software: Sie können es unter den Bedingungen
# der GNU General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
# veröffentlichten Version, weiterverbreiten und/oder modifizieren.
# 
# ToyRegister wird in der Hoffnung, dass es nützlich sein wird, aber
# OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
# Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
# Siehe die GNU General Public License für weitere Details.
# 
# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.

from lcddriver import lcd

# Ansteuerung eines LCD-Displays.
class Display:    
   
    # Konstante für die Anzahl der Zeichen in einer Zeile. 
    LCD_WIDTH = 20
    
    # Initialisierung: Erzeugen einer lcd-Instanz.
    def __init__(self):
        self.lcd = lcd()
        
    # Umschalten der Hintergrundbeleuchtung. state ist ein Wahrheitswert (True oder False)
    def setBacklight(self, state):
        if state == True:
            self.lcd.lcd_backlight("on")
        else:
            self.lcd.lcd_backlight("off")
            
    # Schreiben den Text message in die angegebene Zeile line (1..4)
    def printCentered(self, message, line):
        if len(message) < self.LCD_WIDTH:
            for _ in range((self.LCD_WIDTH - len(message))/2):
                message = " " + message
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd.lcd_display_string(message, line)
        
    # Löschen des gesamtem Display-Inhalts
    def clear(self):
        self.lcd.lcd_clear()