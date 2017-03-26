#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// http://192.168.2.107/robot?motorA=stop&motorB=stop

// WLAN settings
char WiFiNetwork[] = "Jenke";
char WiFiPassword[] = "holladi4";

// wired connections
#define HG7881_A_IA 16
#define HG7881_A_IB 5
#define HG7881_B_IA 4
#define HG7881_B_IB 0
 
// functional connections
#define MOTOR_B_PWM HG7881_B_IA // Motor B PWM Speed
#define MOTOR_B_DIR HG7881_B_IB // Motor B Direction
#define MOTOR_A_PWM HG7881_A_IA // Motor B PWM Speed
#define MOTOR_A_DIR HG7881_A_IB // Motor B Direction
 
// the actual values for "fast" and "slow" depend on the motor
#define PWM_SLOW 50  // arbitrary slow speed PWM duty cycle
#define PWM_FAST 200 // arbitrary fast speed PWM duty cycle
#define DIR_DELAY 1000 // brief delay for abrupt motor changes

ESP8266WebServer server(1234);

void moveA(float speed){
  int value = (int)((1 - speed) * 1000);
  Serial.println( value );
  digitalWrite( MOTOR_A_DIR, HIGH );
  analogWrite( MOTOR_A_PWM, value );
}

void moveB(float speed){
  int value = (int)((1 - speed) * 1000);
  Serial.println( value );
  digitalWrite( MOTOR_B_DIR, HIGH );
  analogWrite( MOTOR_B_PWM, value );
}

void handleRoot() {
  //digitalWrite(led, 1);
  server.send(200, "text/plain", "hello from esp8266!");
  //digitalWrite(led, 0);
}

void handleNotFound(){
 // digitalWrite(led, 1);
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
  //digitalWrite(led, 0);
}

void setup()
{
  Serial.begin( 9600 );
  pinMode( MOTOR_A_DIR, OUTPUT );
  pinMode( MOTOR_A_PWM, OUTPUT );
  pinMode( MOTOR_B_DIR, OUTPUT );
  pinMode( MOTOR_B_PWM, OUTPUT );

   WiFi.mode(WIFI_STA);
  // Attempt to conect to the WiFi network. 
  Serial.println("Connecting to WiFi network.");
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WiFiNetwork, WiFiPassword);              // Connect to WPA2 network
    uint8_t timeout = 10;                         // Set a timeout variable
    while (timeout && (WiFi.status() != WL_CONNECTED)) {
      timeout--;                                  // Decrement timeout
      delay(1000);                                // Delay for one second
    }
  }
 
  Serial.println("Connected to network.");

  server.on("/", handleRoot);

  server.on("/robot", [](){
//    String state = server.arg("motorA");
    String result = "error";
//    if (state == "forward"){
//      forwardA();
//      result = "Ok!";
//    }
//    else if (state == "stop"){
//      stopA();
//      result = "Ok!";
//    }
//    state = server.arg("motorB");
//    if (state == "forward"){
//      forwardB();
//      result = "Ok!";
//    }
//    else if (state == "stop"){
//      stopB();
//      result = "Ok!";
//    }

   if ( server.hasArg("moveA")){
    float speed = server.arg("moveA").toFloat(); 
    moveA(speed);
    result = "Ok!"; 
   }

   if ( server.hasArg("moveB")){
    float speed = server.arg("moveB").toFloat(); 
    moveB(speed);
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
/*EOF*/
