#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// 192.168.2.112:1234/robot?forward=400 -> forward
// 192.168.2.112:1234/robot?left=400 -> left
// 192.168.2.112:1234/robot?right=400 -> right
// 192.168.2.112:1234/robot?blink=1 -> Show blinkenlights

// WLAN settings
char WiFiNetwork[] = "Jenke";
char WiFiPassword[] = "holladi4";

// Motor settings
#define HG7881_A_IA 16
#define HG7881_A_IB 5
#define HG7881_B_IA 4
#define HG7881_B_IB 0
#define MOTOR_B_PWM HG7881_B_IA // Motor B PWM Speed
#define MOTOR_B_DIR HG7881_B_IB // Motor B Direction
#define MOTOR_A_PWM HG7881_A_IA // Motor B PWM Speed
#define MOTOR_A_DIR HG7881_A_IB // Motor B Direction

// Neopixels
#define PIN 2
#define NUMPIXELS 16

ESP8266WebServer server(1234);
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRBW);

void setup()
{
  Serial.begin( 9600 );

  // Motor
  pinMode( MOTOR_A_DIR, OUTPUT );
  pinMode( MOTOR_A_PWM, OUTPUT );
  pinMode( MOTOR_B_DIR, OUTPUT );
  pinMode( MOTOR_B_PWM, OUTPUT );

  // Wifi
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

  // Webserver
  Serial.println("Connected to network.");
  server.on("/", handleRoot);
  server.on("/robot", [](){
    String result = "error";
    if ( server.hasArg("forward")){
      int duration = server.arg("forward").toInt(); 
      forward(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("left")){
      int duration = server.arg("left").toInt(); 
      left(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("right")){
      int duration = server.arg("right").toInt(); 
      right(duration);
      result = "Ok!"; 
    }
    if ( server.hasArg("blink")){
      showBlinkenlightsFun();
      result = "Ok!"; 
    }
    server.send(200, "text/plain", result);
  });
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");

  // Neopixels
  pixels.begin();
  
}
 
void loop()
{ 
  server.handleClient();
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

/**
 * Move the robot forward for a given duration in milliseconds
 */
void forward(int duration)
{
  motorAForward();
  motorBForward(); 
  delay(duration);
  motorAStop();
  motorBStop();
  delay(100);
}

/**
 * Rotate left for a given duration in milliseconds
 */
void left(int duration)
{
  motorAForward();
  motorBBackward(); 
  delay(duration);
  motorAStop();
  motorBStop();
  delay(100);
}

/**
 * Rotate right for a given duration in milliseconds
 */
void right(int duration)
{
  motorABackward();
  motorBForward(); 
  delay(duration);
  motorAStop();
  motorBStop();
  delay(100);
}

void motorAForward(){
  digitalWrite( MOTOR_A_DIR, HIGH );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void motorABackward(){
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, HIGH );
}

void motorAStop(){
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void motorBForward(){
  digitalWrite( MOTOR_B_DIR, HIGH );
  digitalWrite( MOTOR_B_PWM, LOW );
}

void motorBBackward(){
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, HIGH );
}

void motorBStop(){
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, LOW );
}

int redIndex = 0;
int greenIndex = NUMPIXELS/3;
int blueIndex = NUMPIXELS/3*2;

void showBlinkenlightsFun()
{
  for ( int j = 0; j < NUMPIXELS; j++ ){
    for ( int i = 0; i < NUMPIXELS; i++){
      pixels.setPixelColor(i, pixels.Color(0,0,0,0)); // Moderately bright green color.
    }
  
    pixels.setPixelColor(redIndex, pixels.Color(150,0,0,0)); // Moderately bright green color.
    pixels.setPixelColor(greenIndex, pixels.Color(0,150,0,0)); // Moderately bright green color.
    pixels.setPixelColor(blueIndex, pixels.Color(0,0,150,0)); // Moderately bright green color.
    
    redIndex = (redIndex + NUMPIXELS - 1)%NUMPIXELS;
    greenIndex = (greenIndex + 1)%NUMPIXELS;
    blueIndex = (blueIndex + 1)%NUMPIXELS;
    pixels.show();
    delay(100);
  }

  for ( int i = 0; i < NUMPIXELS; i++){
    pixels.setPixelColor(i, pixels.Color(0,0,0,0)); // Moderately bright green color.
  }
  pixels.show();
}

