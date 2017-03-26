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

from button import Button
import datetime
import os
import time
import threading
from album import Album
from output import output
 
class MusicboxApplication(threading.Thread):
    
    # Initialisierung
    def __init__(self, qrCodeScanner, player, display):
        output("Starting init")
        threading.Thread.__init__(self) 
        self.running = True
        self.qrCodeScanner = qrCodeScanner
        self.player = player;
        self.display = display;
        self.current_album = ""
        self.current_song_index = 0;
        self.songs = self.readConfig("songs.config")
        self.buttonPrev = Button(15, self.prevSong);
        self.buttonNext = Button(13, self.nextSong);
        self.buttonStop = Button(11, self.stopSong);
        self.buttonVolumeUp = Button(29, self.volumeUp);
        self.buttonVolumeDown = Button(37, self.volumeDown);
        self.buttonShutdown = Button(18, self.shutdown);
        self.last_interaction_time = datetime.datetime.now()
        output("Init done")
        
    # Einlesen einer Konfiguration (Song-Liste)
    # Format der Konfig-Datei: 
    # - eine Zeile pro Album
    # - <QR-Code-Tag>: <Album-Name>, <Titel1>, <Titel2>, ...
    def readConfig(self, filename):
        f = open(filename, 'r')
        songs_dict = {}
        for line in f:
            tokens = line.split(":") 
            if len(tokens) == 2:
                key = tokens[0]
                songslist = tokens[1].split(",")
                songslist = [ song.replace("\n", "") for song in songslist]
                songslist = [ song.strip() for song in songslist]
                albumname = songslist[0]
                songslist.pop(0)
                songs_dict[key] = Album(albumname, songslist)
        #print(songs_dict)
        print("Read " + str(len(songs_dict)) + " albums.")
        return songs_dict
        
    # Lautstärke leiser
    def volumeDown(self):
        output("Volume down!")
        os.system("amixer set Speaker 5-");
        
    # Laustärke lauter
    def volumeUp(self):
        output("Volume up!")
        os.system("amixer set Speaker 5+");
      
    # Sprung zum vorherigen Song im Album    
    def prevSong(self):
        output("Prev-Button - prev song")
        self.last_interaction_time = datetime.datetime.now()
        if self.current_album in self.songs:
            album = self.songs[self.current_album]
            if self.current_song_index > 0:
                self.current_song_index = self.current_song_index - 1;
                output('{}{}'.format("Playing prev song with index ", self.current_song_index))
                self.player.stop()
                self.player.play(album.titelliste[self.current_song_index]);
                self.printCurrentSong();
            else:
                output("Reached first song of album!");
        else:
            output("Invalid album: " + self.current_album) 
            
    # Sprung zum nächsten Song im Album 
    def nextSong(self):
        output("Next-Button - next song")
        self.last_interaction_time = datetime.datetime.now()
        if self.current_album in self.songs:
            album = self.songs[self.current_album]
            if len(album.titelliste) > self.current_song_index + 1:
                self.current_song_index = self.current_song_index + 1;
                output('{}{}'.format("Playing next song with index ", self.current_song_index))
                self.player.stop()
                self.player.play(album.titelliste[self.current_song_index]);
                self.printCurrentSong();
            else:
                output("Album has no more songs!");
                self.printCurrentSong();
        else:
            output("Invalid album: " + self.current_album)
          
    # System abschalten, Raspberry Pi herunterfahren  
    def shutdown(self):
        output("System Shutdown!")
        self.display.printCentered("Geraet ausgeschaltet", 1);
        self.display.setBacklight(False)
        os.system("sudo shutdown -h now");
            
    # Aktuell laufenden Song beenden
    def stopSong(self):
        output("Stop-Button")
        self.last_interaction_time = datetime.datetime.now()
        self.current_album = "";
        self.current_song_index = 0;
        self.player.stop();
        self.display.clear();
        self.display.printCentered("Album-Code scannen!", 1);
        
    # Zeit seit der letzten Interaktion ausgeben
    def getIdleTime(self):
        return (datetime.datetime.now() - self.last_interaction_time).total_seconds()
       
    # Aktuellen Song auf dem Display ausgeben.
    def printCurrentSong(self):
        self.display.clear()
        if self.current_album in self.songs:
            album = self.songs[self.current_album]
            self.display.printCentered(album.albumname, 1);
            self.display.printCentered("Lied " + str(self.current_song_index + 1), 2);
            return;            
        self.display.printCentered("", 1);
        self.display.printCentered("", 2);
    
    # Nachricht auf dem Display ausgeben.
    def printMessage(self, message):
        self.display.clear()
        self.display.printCentered(message, 1);
        
    # Main-Loop
    def run(self):
        output("Started MusicBox thread.")
        os.system("amixer set Speaker 5");
        self.buttonPrev.start();
        self.buttonNext.start();
        self.buttonStop.start();
        self.buttonVolumeUp.start();
        self.buttonVolumeDown.start();
        self.buttonShutdown.start()
        self.last_interaction_time = datetime.datetime.now()
        self.display.clear();
        self.display.printCentered("Album-Code scannen!", 1);
        self.display.setBacklight(True)
        while self.running:

            # New album scanned
            symbol = self.qrCodeScanner.pullSymbol()
            if symbol != '':
                self.last_interaction_time = datetime.datetime.now()
                self.player.stop()
                
                # Spezialfall: Übergang zur Kinderkassen-App
                if symbol == "startregister":
                    self.running = False;
                    break
                
                self.current_album = symbol
                self.current_song_index = 0
                output("New album detected via QR code: " + self.current_album)
                if self.current_album in self.songs:
                    album = self.songs[self.current_album]
                    if self.current_song_index < len(album.titelliste): 
                        self.player.play(album.titelliste[self.current_song_index]);
                        self.printCurrentSong();
                    else:
                        output("Album " + symbol + " does not contain any songs!")
                else:
                    output("Invalid album: " + self.current_album)
            
            # Song at end -> next song
            if self.current_album in self.songs:
                if self.player.atEnd():
                    output("Song ended - next song")
                    album = self.songs[self.current_album]
                    if self.current_song_index + 1 < len(album.titelliste):
                        self.current_song_index = self.current_song_index + 1
                        output('{}{}'.format("Playing next song with index ", self.current_song_index))
                        self.player.stop(); 
                        self.player.play(album.titelliste[self.current_song_index]);
                        self.last_interaction_time = datetime.datetime.now()
                        self.printCurrentSong();
                else:
                    self.last_interaction_time = datetime.datetime.now()               
                
            time.sleep(0.1)
            
        # Quit
        self.display.clear();
        self.display.printCentered("Tschuess", 1);
        self.player.stop()
        self.buttonPrev.stop()
        self.buttonNext.stop()
        self.buttonStop.stop()
        self.buttonVolumeUp.stop()
        self.buttonVolumeDown.stop()
        self.buttonShutdown.stop()
        output("MusicBox application ended")