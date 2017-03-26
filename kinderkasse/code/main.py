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

from camerapi import CameraPi
from qrcodescanner import QrCodeScanner
from display import Display
from mp3player import Mp3Player
from musicbox_application import MusicboxApplication
from register_application import RegisterApplication
from musicbox_application import output

# Einstiegspunkt für alle Anwendungen

camera = CameraPi()
display = Display()
player = Mp3Player()
qrCodeScanner = QrCodeScanner(camera)
qrCodeScanner.start()
# Über diese globale variable wird zwischen Kinderkasse und MusicBox hin- und hergeschaltet
# QR-Code startmusicbox -> "musicbox"
# QR-Code startregister -> "register" 
 
try:  
    while True:
        # Start mit MusicBox
        app = MusicboxApplication(qrCodeScanner, player, display)
        app.start();
        app.join()
        
        # Dann: Kinderkasse
        app = RegisterApplication(qrCodeScanner, display)
        app.start()
        app.join()

    qrCodeScanner.stop()
    player.end()
    output("Done.")
    
except Exception as inst:
    output("Exception while running the application: ")
    output(str(inst))
    output("Trying again ...")