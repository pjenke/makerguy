#include "programming_pad.h"
#include "Arduino.h"

ProgrammingPad::ProgrammingPad(){
  voltageRatios.add(0.91);
  voltageRatios.add(0.87);
  voltageRatios.add(0.82);
  voltageRatios.add(0.75);

  pins.add(0);
  pins.add(1);
  pins.add(2);
  pins.add(3);
  pins.add(4);
  pins.add(5);
  pins.add(6);
  pins.add(7);
  pins.add(8);
  pins.add(9);
  pins.add(10);
  pins.add(11);
}

/**
 * Creates the current program as a list of the active states.
 */
void ProgrammingPad::assembleCurrentProgram(){
  assembleProcedure1Program();
  currentProgram.clear();
  for ( int pin = 0; pin < 8; pin++ ){
    int stateIndex = getStateIndex(pin);
    if ( stateIndex == PROCEDURE1 ){
      for ( int j = 0; j < procedure1Program.getSize(); j++ ){
        currentProgram.add(procedure1Program.get(j));
      }
    } else if ( stateIndex >= 0 ){
      currentProgram.add(stateIndex);
    }
  }
}

/**
 * Creates the program for procedure 1 as a list of the active states.
 */
void ProgrammingPad::assembleProcedure1Program(){
  procedure1Program.clear();
  for ( int pin = 8; pin < 12; pin++ ){
    int stateIndex = getStateIndex(pin);
    if ( stateIndex >= 0 ){
      procedure1Program.add(stateIndex);
    }
  }
}

/**
 * Print the current program to the console.
 */
void ProgrammingPad::printCurrentProgram(){
  Serial.print("Program: ");
  for ( int i = 0; i < currentProgram.getSize(); i++ ){
    printState(currentProgram.get(i));
  }

  Serial.print("(proc1: ");
  for ( int i = 0; i < procedure1Program.getSize(); i++ ){
    printState(procedure1Program.get(i));
  }
  Serial.print(")");
  
  Serial.println();
}

/**
 * Prints the board with all its states. 
 */
void ProgrammingPad::printBoard(){
  Serial.println("<--- BOARD --->");
  printPin(3); printPin(7);  printPin(11);
  Serial.println();
  printPin(2); printPin(6);  printPin(10);
  Serial.println();
  printPin(1); printPin(5);  printPin(9);
  Serial.println();
  printPin(0); printPin(4);  printPin(8);
  Serial.println();
  Serial.println("<------------->");
}

/**
 * Returns the state index for the given pin. -1 indicates invalid state.
 */
int ProgrammingPad::getStateIndex(int pin) {
  int val = analogRead(pins.get(pin));
  double voltage = (float)val/1024.0;
  for ( int i = 0; i < voltageRatios.getSize(); i++ ){
    if ( abs(voltage-voltageRatios.get(i)) <= EPSILON ){
      return i;
    }
  }
  return -1;
}

/**
 * Prints the state of the given pin to the console.
 */
void ProgrammingPad::printPin(int pin){
  int stateIndex = getStateIndex(pin);
  printState(stateIndex);
}

/**
 * Prints a human-readable state represenaion for a state index.
 */
void ProgrammingPad::printState(int stateIndex){
  Serial.print(getStateName(stateIndex));
}

/**
 * Returns a human-readbly state representation for a state index.
 */
String ProgrammingPad::getStateName(int stateIndex){
  if ( stateIndex == 0 ){
    return " [^] ";
  } else if ( stateIndex == 1 ){
    return " [<] ";
  } else if ( stateIndex == 2 ){
    return " [>] ";
  } else if ( stateIndex == 3 ){
    return " [1] ";
  } else {
    return " [ ] ";
  }
}

String ProgrammingPad::getCurrentCommand(){
  String command = "";
  for ( int i = 0; i < currentProgram.getSize(); i++ ){
    int stateIndex = currentProgram.get(i);
    if ( stateIndex == 0 ){
      command += "F";
    } else if ( stateIndex == 1 ){
      command += "L";
    } else if ( stateIndex == 2 ){
      command += "R";
    }
  }
  command += "B";
  return command;
}

