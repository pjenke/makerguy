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

import zbar, threading, time 
from thread import allocate_lock

# Der QrCodeScanner läuft als Thread und prüft kontinuierlich, ob er im aktuellen
# Kamera-Frame eine QR-Code finden kann.
#
# siehe auch: http://zbar.sourceforge.net/api/classzbar_1_1ImageScanner.html
class QrCodeScanner(threading.Thread):
    
    # Initialisierung
    def __init__(self, camera):
        threading.Thread.__init__(self)
        # Erzeugen erzeugen einer Scanner-Instanz, die in einem Bild nach QR-Codes sucht. 
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')
        self.camera = camera
        self.lastSymbol = ''
        # Get a locking handle
        self.lock = allocate_lock()
        self._stop = threading.Event()
        self.daemon = True
        self.isRunning = True
      
    # Gefundene Symbole werden zwischengespeichert. Die Methode ist synchronisiert.  
    def pushSymbol(self, symbol):
        self.lock.acquire()
        self.lastSymbol = symbol
        self.lock.release()
        
    # Abrufen des letzten gespeicherten Symbols. Liefert '' falls aktuell kein Symbol
    # bereit ist. Die Methode ist synchronisiert.  
    def pullSymbol(self):
        self.lock.acquire()
        symbol = self.lastSymbol
        self.lastSymbol = ''
        self.lock.release()
        return symbol
        
    # Scanner-Loop
    def run(self):
        while self.isRunning:
            # Wartezeit zwischen zwei Aufnahmen.
            time.sleep(0.1)
            # Auslesen eines Kamerabildes, Konvertieren in ein zbar-kompabibles Format
            pil = self.camera.grabImage()
            pil = pil.convert('L')
            width, height = pil.size
            raw = pil.tostring()
            image = zbar.Image(width, height, 'Y800', raw)
            # Scannen des Eingabebildes
            self.scanner.scan(image)
            # Falls im Bild ein Symbol gefunden wurde, wird sich dies gemerkt
            for s in image:
                self.pushSymbol(s.data)
            # Cleanup
            del(image)
            
            # 5 Sekunden warten, wenn ein Symbol gefunden wurde
            if self.lastSymbol != '':
                time.sleep(5)
    
    def stop(self):
        self.isRunning = False;
        self._stop.set()