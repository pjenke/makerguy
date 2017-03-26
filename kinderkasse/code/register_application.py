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

import threading
from product import Product
from output import output
from button import Button
import os

# Eine Kassen-Anwendung hat einen internen Warenkorb und man kann sich die Summe
# aller bereits erworbenen (gescannten) Waren im Warenkorb ausgeben lassen.
class RegisterApplication(threading.Thread):

    # Initialisierung
    def __init__(self, qrcodescanner, display):
        threading.Thread.__init__(self) 
        self.cart = []
        self.qrcodescanner = qrcodescanner
        self.display = display
        self.allProducts = [Product("milch", "Milch", 1.49), 
                            Product("butter", "Butter", 0.89),
                            Product("apfel", "Apfel", 0.79),
                            Product("schokolade", "Schokolade", 1.29)]
        self.buttonQuit = Button(37, self.quit);
        self.buttonOne = Button(15, self.numberOne)
        self.buttonTwo = Button(13, self.numberTwo)
        self.buttonThree = Button(11, self.numberThree)
        self.buttonFour = Button(35, self.numberFour)
        self.buttonFive = Button(33, self.numberFive)
        self.buttonSix = Button(31, self.numberSix)
        self.buttonSeven = Button(18, self.numberSeven)
        self.buttonEight = Button(16, self.numberEight)
        self.buttonNine = Button(12, self.numberNine)
        self.buttonZero = Button(7, self.numberZero)
        self.buttonAccept = Button(29, self.accept)
        self.current_amount = "";
        self.isRunning = True
        
    def addProductToCart(self, product):
        self.cart.append(product)
        
    def getAmount(self):
        amount = 0;
        for product in self.cart:
            amount += product.amount
        return amount
    
    def getProductForSymbol(self, symbol):
        for product in self.allProducts:
            if product.tag == symbol:
                return product
        return -1
    
    def numberOne(self):
        self.number(1);
    
    def numberTwo(self):
        self.number(2);
        
    def numberThree(self):
        self.number(3);
        
    def numberFour(self):
        self.number(4);
        
    def numberFive(self):
        self.number(5);
        
    def numberSix(self):
        self.number(6);
        
    def numberSeven(self):
        self.number(7);
        
    def numberEight(self):
        self.number(8);
        
    def numberNine(self):
        self.number(9);
        
    def numberZero(self):
        self.number(0);
        
    def accept(self):
        if len(self.current_amount) < 3:
            self.display.clear()
            self.display.printCentered("Mindestens 3 Ziffern", 2);
            return
        amount = float(self.makeFloatingPoint(self.current_amount))
        product = Product("", "Manuell", amount)
        self.addProductToCart(product)
        self.printProductState(product)
        self.current_amount = ""
    
    def makeFloatingPoint(self, amount):
        if len(amount) == 0:
            return 0
        elif len(amount) == 1:
            return float("0.0" + amount)
        elif len(amount) == 2:
            return float("0." + amount)
        else: 
            return float(amount[:-2] + "." + amount[-2:] )
    
    def number(self, num):
        self.current_amount = self.current_amount + str(num)
        self.display.clear()
        self.display.printCentered(str(self.makeFloatingPoint(self.current_amount)), 2);
        
    def printProductState(self, product):
        self.display.clear()
        self.display.printCentered(product.name + " (" + str(product.amount) + ")", 1);
        self.display.printCentered(str(len(self.cart)) + " Produkt(e)", 2);
        self.display.printCentered("Summe: " + str(self.getAmount()), 3);
        
    # System abschalten, Raspberry Pi herunterfahren  
    def shutdown(self):
        output("System Shutdown!")
        self.display.printCentered("Geraet ausgeschaltet", 1);
        self.display.setBacklight(False)
        self.running = False
        os.system("sudo shutdown -h now");
        
    def run(self):
        output("Started Register thread.")
        self.display.clear()
        self.display.printCentered("Willkommen bei", 1)
        self.display.printCentered("der Kinderkasse", 2)
    
        self.buttonQuit.start()
        self.buttonOne.start()
        self.buttonTwo.start()
        self.buttonThree.start()
        self.buttonFour.start()
        self.buttonFive.start()
        self.buttonSix.start()
        self.buttonSeven.start()
        self.buttonEight.start()
        self.buttonNine.start()
        self.buttonZero.start()
        self.buttonAccept.start()
        
        while self.isRunning:
            symbol = self.qrcodescanner.pullSymbol()
            
            # Spezialfall: Übergang zur MusicBox-App
            if symbol == "startmusicbox":
                self.running = False;
                break
            
            product = self.getProductForSymbol(symbol)
            if product != -1:
                self.addProductToCart(product)
                self.printProductState(product)
        output("Quitting Register application")
        self.display.clear()
        self.display.printCentered("Tschuess", 1);
        self.buttonQuit.stop()
        self.buttonOne.stop()
        self.buttonTwo.stop()
        self.buttonThree.stop()
        self.buttonFour.stop()
        self.buttonFive.stop()
        self.buttonSix.stop()
        self.buttonSeven.stop()
        self.buttonEight.stop()
        self.buttonNine.stop()
        self.buttonZero.stop()
        self.buttonAccept.stop()
        # Diese Zeile auskommentieren, wenn man beim Beenden nicht den Pi ausschalten will
        #self.shutdown()
        output("Register application ended")
                
    def quit(self):
        self.isRunning = False