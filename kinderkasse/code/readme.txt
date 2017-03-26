*** TASTENBELEGUNG ***
Benennung der Tasten in dieser Doku (Blick von vorne auf die Kinderkasse):
a b c d 
e f g h
i j k l
- Pin-Belegung:
a: 15, b: 13, c: 11, d: 7
e: 35, f: 33, g: 31, h: 29
i: 18, j: 16, k: 12, l: 37

*** MUSIC-BOX ***
Anwendung: musicbox_application.py
Tastenbelegung:
a: Vorheriges Lied im Album
b: Nächstes Lied im Album
c: Stop
h: Lauter
l: Leiser
i: Raspberry Pi ausschalten

*** KINDER-KASSE ***
Anwendung: register_application.py
Tastenbelegung:
a: 1
b: 2
c: 3
e: 4
f: 5
g: 6
i: 7
j: 8
k: 9
d: 0
h: Produkt akzeptieren
l: Raspberry Pi ausschalten
Bedienung:
- Möglichkeit 1: QR-Code mit Produkt-Tag scannen: Produkt wird in den Warenkorb 
gelegt, Produkt und Warenkorbsumme werden angezeigt
- Möglichkeit 2: Preis über Ziffer-Tasten eingeben. Eingabe von rechts nach links 
(Cent-Betrag zuerst), nach zwei Ziffern wird automatisch ein Komma hinzugefügt. 
Erstellen eines Produktes (Name: "Manuell") durch Druck auf die Akzeptieren-Taste.