import time

# Ausgabe einer Debug-Meldung (aktuell: Konsole + Log-File)
def output(message):
    # Console
    message = "[" + time.strftime("%c") + "] " + message;
    print(message);
    # Logfile
    f = open("log.txt", "a")
    f.write(message + "\n");
    f.close();