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

import RPi.GPIO as GPIO, threading, time
from output import output

# Die Klasse Butten repräsentiert einen Taster, der mit einem GPIO-Pin verbunden ist. Sie ist
# als Thread umgesetzt und prüft permanent, ob sich der Zustand des GPIOs verändert, was einem
# Tastendruck entsproch. Wurde ein Tastendruck festgestellt, wird eine Routine zur Behandlung 
# dieses Ereignisses aufgerufen (Referenz auf eine Funktion). 
class Button(threading.Thread):    
    def __init__(self, pin, eventHandler): 
        threading.Thread.__init__(self) 
        self.pin = pin
        self.eventHandler = eventHandler
        # Standard-Wert (Taster nicht gedrückt): LOW
        self.lastState = GPIO.LOW
        GPIO.setmode(GPIO.BOARD)
        # GPIO wird als Input verwendet
        GPIO.setup(pin, GPIO.IN) 
        self._stop = threading.Event()
        self.daemon = True
        self.isRunning = True
        
    def run(self):
        output("Button thread started")
        while self.isRunning:
            # Die Überprüfung des Zustandes findet alle 0.5s statt
            time.sleep(0.1)
            # Der letzte Zustand des GPIO wird protokolliert, hier zurückgesetzt. 
            # Der Zustand HIGH zeigt, dass der Taster nicht gedrückt ist.
            if ( GPIO.input(self.pin) == GPIO.HIGH):
                self.lastState = GPIO.HIGH
            # Wenn der Zustand auf LOW wechselt, wurde der Taster gedrückt; die Routine
            # zum Behandeln des Ereignisses wird aufgerufen 
            if ( GPIO.input(self.pin) == GPIO.LOW and self.lastState == GPIO.HIGH ):
                self.lastState = GPIO.LOW
                # Aufrufen der Ereignis-Verarbeitung 
                self.eventHandler()
                # Kurze Pause, bis die nächste Zustandsänderung abgeprüft wird
                time.sleep(1)
        output("Button thread ended")
    
    # Stop the thread            
    def stop(self):
        self.isRunning = False
        self._stop.set()