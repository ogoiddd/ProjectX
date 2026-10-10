import java.util.List;

interface Ilayout {
    /** Return the configurations reachable in one legal move. */
    List<Ilayout> children();
    /** Return true if this configuration is a goal configuration. */
    boolean isGoal(Ilayout l);
    /** Cost of moving into this configuration: 1 for this puzzle. */
    double getK();
}
