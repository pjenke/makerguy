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

import io, time, picamera, PIL.Image

# Die CameraPi-Klasse ist ein Wrapper für die picamera-Klasse. Es werden die notwendigen 
# Kamera-Einstellungen vorgenommen und es wird ein einfacher Zugrff auf Kamera-Frames
# bereitgestellt.
#
# siehe auch: picamera.readthedocs.io/en/release-1.10/api_camera.html 
# siehe auch: http://effbot.org/imagingbook/image.htm
class CameraPi:
    
    def __init__(self):
        # Instanziieren eines Kamera-Objektes
        self.camera = picamera.PiCamera();
        # Festlegen der Auflösung der geschossenen Bilder
        self.camera.resolution = (640, 480)
        
        # Starten der kontinuierlichen Aufnahme, nicht benötigt, oder?
        self.camera.start_preview()
        
        time.sleep(2)
    
    def grabImage(self):
        # Erzeugen eines Streams, der ein Kamera-Frame vorhalten soll
        stream = io.BytesIO()
        # Ablegen des neusten Kamera-Frames als JPEG 
        self.camera.capture(stream, format='jpeg', resize=(640, 480))
        # Stream zum Lesen 'zurückspulen'
        stream.seek(0)
        # Bild-Instanz erzeugen
        image = PIL.Image.open(stream)
        return image

# Debugging: Kamera-Frame als Bild abspeichern.
class CameraFile:
    def grabImage(self):
        return PIL.Image.open('test.jpg')