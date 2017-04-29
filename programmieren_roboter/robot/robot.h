#ifndef ROBOT_H
#define ROBOT_H

#include <Adafruit_NeoPixel.h>

// Motor settings
#define HG7881_A_IA 16
#define HG7881_A_IB 5
#define HG7881_B_IA 4
#define HG7881_B_IB 0
#define MOTOR_B_PWM HG7881_B_IA // Motor B PWM Speed
#define MOTOR_B_DIR HG7881_B_IB // Motor B Direction
#define MOTOR_A_PWM HG7881_A_IA // Motor B PWM Speed
#define MOTOR_A_DIR HG7881_A_IB // Motor B Direction

#define FORWARD_DURATION 2100 // Calibration!
#define LEFT_DURATION 1210 // Calibration!
#define RIGHT_DURATION 1300 // Calibration!

// Neopixels
#define PIN 2
#define NUMPIXELS 16

class Robot {
  private:
    Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRBW);

    void motorBStop();
    void motorBBackward();
    void motorBForward();
    void motorAStop();
    void motorABackward();
    void motorAForward();
    
  public:
    /** Constructor */
    Robot();

    /**
     * Play a RGB animation.
     */
    void showBlinkenlightsFun();

    /**
     * Move one field forwards.
     */
    void forward();

    /**
     * Turn left 90 degrees.
     */
    void left();

    /**
     * Turn right 90 degrees.
     */
    void right();

    /**
     * Move forward for the given duration in milliseconds.
     */
    void forward(int duration);

    /**
     * Turn left for the given duration in milliseconds.
     */
    void left(int duration);

    /**
     * Turn right for the given duration in milliseconds.
     */
    void right(int duration);
};
#endif
