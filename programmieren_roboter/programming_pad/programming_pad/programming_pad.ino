// https://github.com/bportaluri/WiFiEsp - building upon example WebClient
#include "WiFiEsp.h"
#include "programming_pad.h"

// WIFI
const char* ssid = "Jenke";
const char* password = "holladi4";
const char* host = "http://users.informatik.haw-hamburg.de/~abo781/";
int status = WL_IDLE_STATUS; // the Wifi radio's status
char server[] = "192.168.2.120"; // robot
int port = 1234;
WiFiEspClient client;

ProgrammingPad programmingPad;

/**
 * Arduino sketch initialization.
 */
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(115200);

  initWifi();
}

/**
 * Arduino main loop.
 */
void loop() { 
  handleProgramStartButtonDebug();
}

void initWifi(){
  WiFi.init(&Serial1);   // initialize ESP serial port
  if (WiFi.status() == WL_NO_SHIELD) {   // check for the presence of the shield
    Serial.println("WiFi shield not present");
    while (true);                        // don't continue:
  }

  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    //WiFi.hostname("programming_pad")
    status = WiFi.begin(ssid, password);
  }

  // you're connected now, so print out the data
  Serial.println("You're connected to the network");
  
  printWifiStatus();
}

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

/**
 * Handle the start button on the programming board
 */
void handleProgramStartButtonDebug(){
  if ( digitalRead(BUTTON_PIN) == HIGH ){
    /// TEST
    Serial.println();
    Serial.println("Starting connection to server...");
    // if you get a connection, report back via serial
    if (client.connect(server, port)) {
      Serial.println("Connected to server");
      // Make a HTTP request
      client.println("GET /robot?command=BFLB HTTP/1.1");
      client.println("Host: robot");
      client.println("Connection: close");
      client.println();
      Serial.println("Request done.");
      client.flush();
      client.stop();
    }
  }
}

/**
 * Handle the start button on the programming board
 */
void handleProgramStartButton(){
  if ( digitalRead(BUTTON_PIN) == HIGH ){
    programmingPad.printBoard();
    programmingPad.assembleCurrentProgram();
    programmingPad.printCurrentProgram();  
    Serial.println();
    delay(1000);
    Serial.println("Press button to print board status ...");
  }
}
