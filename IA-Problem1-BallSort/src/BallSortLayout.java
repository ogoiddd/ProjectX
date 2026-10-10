import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class BallSortLayout implements Ilayout, Cloneable {
    private static final char EMPTY = 'E';
    private int height;          // capacity of each tube
    private char[][] tubes;      // tubes[t][0] is the bottom ball of tube t
    private int[] size;          // number of balls in each tube

    /** Build a layout from H lines (top to bottom), each with T colors separated by one space. */
    public BallSortLayout(String str) throws IllegalStateException {
        String[] rows = str.split("\n");
        height = rows.length;
        if (height == 0) throw new IllegalStateException("Invalid arg in BallSortLayout constructor");
        int nTubes = rows[0].split(" ").length;
        tubes = new char[nTubes][height];
        size = new int[nTubes];
        // Read each tube from the bottom row up to the top row.
        for (int r = height - 1; r >= 0; r--) {
            String[] cells = rows[r].split(" ");
            if (cells.length != nTubes)
                throw new IllegalStateException("Invalid arg in BallSortLayout constructor");
            for (int t = 0; t < nTubes; t++) {
                char c = cells[t].charAt(0);
                if (c != EMPTY) tubes[t][size[t]++] = c;
            }
        }
    }

    private BallSortLayout(int height, char[][] tubes, int[] size) {
        this.height = height;
        this.tubes = tubes;
        this.size = size;
    }

    @Override
    protected BallSortLayout clone() {
        char[][] t = new char[tubes.length][];
        for (int i = 0; i < tubes.length; i++) t[i] = tubes[i].clone();
        return new BallSortLayout(height, t, size.clone());
    }

    /** H rows from top to bottom; colors separated by one space; newline after each row. */
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int r = height - 1; r >= 0; r--) {
            for (int t = 0; t < tubes.length; t++) {
                if (t > 0) sb.append(' ');
                sb.append(r < size[t] ? tubes[t][r] : EMPTY);
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BallSortLayout b = (BallSortLayout) o;
        return height == b.height && Arrays.equals(size, b.size) && Arrays.deepEquals(tubes, b.tubes);
    }

    public int hashCode() {
        return 31 * Arrays.hashCode(size) + Arrays.deepHashCode(tubes);
    }

    /** Every legal move: take the top ball of tube i and push it onto tube j
     *  if j is not full and is either empty or has a top ball of the same color. */
    public List<Ilayout> children() {
        List<Ilayout> children = new ArrayList<>();
        for (int i = 0; i < tubes.length; i++) {
            if (size[i] == 0) continue;
            char ball = tubes[i][size[i] - 1];
            for (int j = 0; j < tubes.length; j++) {
                if (j == i || size[j] == height) continue;
                if (size[j] > 0 && tubes[j][size[j] - 1] != ball) continue;
                BallSortLayout child = clone();
                child.tubes[i][--child.size[i]] = 0;
                child.tubes[j][child.size[j]++] = ball;
                children.add(child);
            }
        }
        return children;
    }

    /** The goal does not depend on l: every tube must be empty or full of a single color. */
    public boolean isGoal(Ilayout l) {
        for (int t = 0; t < tubes.length; t++) {
            if (size[t] == 0) continue;
            if (size[t] != height) return false;
            for (int k = 1; k < height; k++)
                if (tubes[t][k] != tubes[t][0]) return false;
        }
        return true;
    }

    public double getK() {
        return 1;
    }
}
