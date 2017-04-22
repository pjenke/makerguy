
public class VoltageDivider implements Comparable<VoltageDivider> {
  public int r1;
  public int r2;

  public VoltageDivider(int r1, int r2) {
    this.r1 = r1;
    this.r2 = r2;
  }

  @Override
  public int compareTo(VoltageDivider other) {
    if (voltageRatio() < other.voltageRatio()) {
      return -1;
    } else if (voltageRatio() > other.voltageRatio()) {
      return 1;
    } else {
      return 0;
    }
  }

  public double voltageRatio() {
    return (double) r1 / (double) (r1 + r2);
  }

  public String toString() {
    return r1 + "Ω, " + r2 + "Ω ("
        + String.format("voltage ratio(R1): %.2f", voltageRatio()) + ")";
  }

  /**
   * Return the current over R1 in mA.
   * 
   * @param voltage
   */
  public double getCurrentOver(double voltage) {
    return voltage / (r1 + r2) * 1000;
  }
}
