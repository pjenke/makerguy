//#include <SoftwareSerial.h>

// Motor settings
#define MOTOR_A_PWM 5
#define MOTOR_A_DIR 4
#define MOTOR_B_PWM 3
#define MOTOR_B_DIR 2
//#define rxPin 10
//#define txPin 11
#define ONBOARD_LED_PIN 13

//SoftwareSerial btSerial(rxPin, txPin);
String btData;

void setup()
{
  Serial.begin(9600);
  pinMode( MOTOR_A_DIR, OUTPUT );
  pinMode( MOTOR_A_PWM, OUTPUT );
  pinMode( MOTOR_B_DIR, OUTPUT );
  pinMode( MOTOR_B_PWM, OUTPUT );
  pinMode( ONBOARD_LED_PIN, OUTPUT );
}

void loop()
{ 
  handleBluetoothDebug();
  //handleBluetooth();
  //debugControlMotors();
}

void handleBluetoothDebug(){
  if (Serial.available() > 0){
    byte val = Serial.read();
    digitalWrite(ONBOARD_LED_PIN, HIGH);
    motorASpeed(100);
    delay(500);
    digitalWrite(ONBOARD_LED_PIN, LOW);
    motorASpeed(0);
  }
}

void handleBluetooth(){
  if (Serial.available() > 0){
//    int code = Serial.read();
//    motorASpeed(code);
//    Serial.println("Motor A: " + code);
    
    btData = Serial.readString();
      if(btData.startsWith("left")){
        int value = btData.substring(4).toInt();
        motorASpeed(value);
      } else if (btData.startsWith("right")){
        int value = btData.substring(5).toInt();
        motorBSpeed(value);
      } else if ( btData.startsWith("on") ){
        digitalWrite(ONBOARD_LED_PIN, HIGH);
      } else if ( btData.startsWith("off") ){
        digitalWrite(ONBOARD_LED_PIN, LOW);
      }
  }
}
 


void debugControlMotors(){
  for ( int i = 0; i < 100; i+= 1){
    motorASpeed(i);
    motorBSpeed(i);
    delay(30);
  }
  motorASpeed(0);
  motorBSpeed(0);
  delay(2000);
}

/**
 * Valid values between 0 (stop) and 100 (full speed).
 */
void motorASpeed(int throttle){
  if (throttle == 0){ 
    digitalWrite( MOTOR_A_PWM, LOW);
    digitalWrite( MOTOR_A_DIR, LOW );
  } else {
    int startVal = 75;
    int maxVal = 255;
    analogWrite( MOTOR_A_PWM,  startVal + throttle / 100.0 * (maxVal - startVal));
    digitalWrite( MOTOR_A_DIR, LOW );
  }
}

/**
 * Valid values between 0 (stop) and 100 (full speed).
 */
void motorBSpeed(int throttle){
  if (throttle == 0){ 
    digitalWrite( MOTOR_B_PWM,  LOW);
    digitalWrite( MOTOR_B_DIR, LOW );
  } else {
    int startVal = 50;
    int maxVal = 255;
    analogWrite( MOTOR_B_PWM,  startVal + throttle / 100.0 * (maxVal - startVal));
    digitalWrite( MOTOR_B_DIR, LOW );
  }
}



void forward(int duration)
{
  motorAForward();
  motorBForward(); 
  delay(duration);
  motorBStop();
  motorAStop();
  delay(100);
}

void motorAForward(){
  digitalWrite( MOTOR_A_DIR, HIGH );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void motorAStop(){
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void motorBForward(){
  digitalWrite( MOTOR_B_DIR, HIGH );
  digitalWrite( MOTOR_B_PWM, LOW );
}

void motorBStop(){
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, LOW );
}
