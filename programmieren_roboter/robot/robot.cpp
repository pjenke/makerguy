#include "robot.h"
#include "Arduino.h"

Robot::Robot(){
  // Motors
  pinMode( MOTOR_A_DIR, OUTPUT );
  pinMode( MOTOR_A_PWM, OUTPUT );
  pinMode( MOTOR_B_DIR, OUTPUT );
  pinMode( MOTOR_B_PWM, OUTPUT );
  // Neopixels
  pixels.begin(); 
}

void Robot::forward(){
  forward(FORWARD_DURATION);
}

void Robot::left(){
  left(LEFT_DURATION);
}

void Robot::right(){
  right(RIGHT_DURATION);
}

/**
 * Move the robot forward for a given duration in milliseconds
 */
void Robot::forward(int duration)
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
void Robot::left(int duration)
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
void Robot::right(int duration)
{
  motorABackward();
  motorBForward(); 
  delay(duration);
  motorAStop();
  motorBStop();
  delay(100);
}

void Robot::motorAForward(){
  digitalWrite( MOTOR_A_DIR, HIGH );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void Robot::motorABackward(){
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, HIGH );
}

void Robot::motorAStop(){
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, LOW );
}

void Robot::motorBForward(){
  digitalWrite( MOTOR_B_DIR, HIGH );
  digitalWrite( MOTOR_B_PWM, LOW );
}

void Robot::motorBBackward(){
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, HIGH );
}

void Robot::motorBStop(){
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, LOW );
}

void Robot::showBlinkenlightsFun()
{
  int redIndex = 0;
  int greenIndex = NUMPIXELS/3;
  int blueIndex = NUMPIXELS/3*2;
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
