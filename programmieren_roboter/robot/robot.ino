#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
extern "C" {
  #include "user_interface.h"
}
#include "robot.h"

// 192.168.2.112:1234/robot?forward=400 -> forward
// 192.168.2.112:1234/robot?left=400 -> left
// 192.168.2.112:1234/robot?right=400 -> right
// 192.168.2.112:1234/robot?blink=1 -> Show blinkenlights
// 192.168.2.112:1234/robot?command=BFLR -> B = Blink, F = Forward, L = Left, R = Right

// WLAN settings
char WiFiNetwork[] = "Jenke";
char WiFiPassword[] = "holladi4";
char wiFiHostname[] = "robot";

Robot robot;

ESP8266WebServer server(1234);

void setup()
{
  Serial.begin( 9600 );

  // Wifi
  WiFi.mode(WIFI_STA);
  // Attempt to conect to the WiFi network. 
  Serial.println("Connecting to WiFi network.");
  wifi_station_set_hostname(wiFiHostname);
  WiFi.hostname(wiFiHostname);
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WiFiNetwork, WiFiPassword);              // Connect to WPA2 network
    uint8_t timeout = 10;                         // Set a timeout variable
    while (timeout && (WiFi.status() != WL_CONNECTED)) {
      timeout--;                                  // Decrement timeout
      delay(1000);                                // Delay for one second
    }
  }

  // Webserver
  Serial.println("Connected to network.");
  server.on("/", handleRoot);
  server.on("/robot", [](){
    String result = "error";
    if ( server.hasArg("forward")){
      int duration = server.arg("forward").toInt(); 
      robot.forward(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("left")){
      int duration = server.arg("left").toInt(); 
      robot.left(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("right")){
      int duration = server.arg("right").toInt(); 
      robot.right(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("blink")){
      robot.showBlinkenlightsFun();
      result = "Ok!"; 
    }
    if ( server.hasArg("command")){
      String commands = server.arg("command"); 
      handleCommands(commands);
      result = "Ok!"; 
    }
    server.send(200, "text/plain", result);
  });
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop()
{ 
  server.handleClient();
}

void handleCommands(String commands){
  for ( int i = 0; i < commands.length(); i++ ){
    char command = commands.charAt(i);
    if ( command == 'B' ){
      robot.showBlinkenlightsFun();
    } else if ( command == 'F' ){
      robot.forward();
    } else if ( command == 'L' ){
      robot.left();
    } else if ( command == 'R' ){
      robot.right();
    }
    delay(500);
  }
}

void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}
