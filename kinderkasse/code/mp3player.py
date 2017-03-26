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

import subprocess
from output import output

# Die Klasse erlaubt es, MP3-Dateien abzuspielen. Dazu wird das Kommandozeilenwerkzeug 
# mpg321 verwendet.
#
# siehe: http://mpg321.sourceforge.net/
class Mp3Player:
    def __init__(self):
        self.process = None
    
    # Spielt einen Song aus einer MP3-Datei
    def play(self, filename):
        output('Playing ' + filename)
        if self.process != None:
            self.process.kill()
        self.process = subprocess.Popen(['mpg321', filename])

    # Stop das Abspielen des aktuellen Songs.
    def stop(self):
        output('Stopped playing.')
        if self.process != None:
            # Returncode = None, solange der Subprozess noch läuft
            if self.process.returncode == None:
                self.process.terminate()
                self.process.kill()
        self.process = None;
        
    # Liefert wahr, wenn das Abspielen eines Songs abgeschlossen ist
    def atEnd(self):
        if self.process != None:
            self.process.poll()
            if self.process.returncode != None:
                return True;
        return False;
    
    def end(self):
        if self.process != None:
            self.process.kill()