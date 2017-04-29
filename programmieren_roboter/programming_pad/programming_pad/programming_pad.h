#ifndef PROGRAMMING_PAD_H
#define PROGRAMMING_PAD_H

#include "indexed_list.h"

// Offset to dedtermine the command by the voltage ratios
#define EPSILON 0.01

// Valid command on the programming board
#define FORWARD 0
#define LEFT 1
#define RIGHT 2
#define PROCEDURE1 3

#define BUTTON_PIN 22

class ProgrammingPad {
  private:
    /** 
     * List of voltage ratios for the different command. 
     */
    IndexedList<double> voltageRatios;
    
    /** 
     * List of A<i> pins on the board for the command.
     */
    IndexedList<int> pins;
    
    /** 
     * List of command indices for the current program. 
     */
    IndexedList<int> currentProgram;
    
    /** 
     *  List of command indices for the proc1 program.
     */
    IndexedList<int> procedure1Program;

    /**
     * Prints a human-readable state represenaion for a state index.
     */
    void printState(int stateIndex);

    /**
     * Prints the state of the given pin to the console.
     */
    void printPin(int pin);

    /**
     * Creates the program for procedure 1 as a list of the active states.
     */
    void assembleProcedure1Program();

    /**
     * Returns the state index for the given pin. -1 indicates invalid state.
     */
    int getStateIndex(int pin);

    /**
     * Returns a human-readbly state representation for a state index.
     */
    String getStateName(int stateIndex);
    
  public:
  /**
   * Constructor
   */
   ProgrammingPad();

   /**
    * Creates the current program as a list of the active states.
    */
    void assembleCurrentProgram();

    /**
     * Prints the board with all its states. 
     */
    void printBoard();

    /**
     * Print the current program to the console.
     */
    void printCurrentProgram();

    /**
     * Returns the command string for the current board setup.
     * B = Blink
     * F = Forward
     * L = Left
     * R = Right
     */
    String getCurrentCommand();
};

#endif
