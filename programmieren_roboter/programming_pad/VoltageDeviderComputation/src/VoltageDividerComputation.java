import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class VoltageDividerComputation {

  public static final int NUMBER_OF_STATES = 8;
  public static final double VOLTAGE = 5;

  public static int getState(double voltage) {
    double delta = 1.0 / (NUMBER_OF_STATES + 2);
    return (int) Math.round((voltage - delta * 1.5) / delta);
  }

  public static void main(String[] args) {
    List<Integer> resistors = Arrays.asList(1000, 1500, 2200, 3300, 3900, 4700,
        5600, 6800, 7500, 8200, 10000);

    List<VoltageDivider> dividers = new ArrayList<VoltageDivider>();
    for (int i = 0; i < resistors.size(); i++) {
      // for (int j = 0; j < resistors.size(); j++) {
      dividers.add(new VoltageDivider(10000, resistors.get(i)));
      // }
    }

    for (int i = 0; i < dividers.size(); i++) {
      VoltageDivider divider = dividers.get(i);
      System.out.format("State %d -> " + divider + ", current: %.2fmA\n", i,
          divider.getCurrentOver(VOLTAGE));
    }

//    Collections.sort(dividers);
//
//    double delta = 1.0 / (NUMBER_OF_STATES + 2);
//    for (int i = 0; i < NUMBER_OF_STATES; i++) {
//      double intervalMiddle = (i + 1.5) * delta;
//      int bestIndex = -1;
//      for (int j = 0; j < dividers.size(); j++) {
//        if (bestIndex < 0
//            || Math.abs(dividers.get(j).voltageRatio() - intervalMiddle) < Math
//                .abs(dividers.get(bestIndex).voltageRatio() - intervalMiddle)) {
//          bestIndex = j;
//        }
//      }
//
//      VoltageDivider divider = dividers.get(bestIndex);
//      System.out.format(
//          "State %d: [%.2f, %.2f], %.2f -> " + divider + ", current: %.2fmA\n",
//          i, (i + 1) * delta, (i + 2) * delta, intervalMiddle,
//          divider.getCurrentOver(VOLTAGE));
//    }
//
//    double voltage = 0.15;
//    System.out.println();
//    System.out.println("*** State-Test ***");
//    System.out.println(voltage + " -> State " + getState(voltage));
  }

}
