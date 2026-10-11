// IA 2026/27 - Problem 1: Ball Sort Puzzle - a88432
// AI use declaration (FUC / UAlg AI policy): code written with the assistance
// of Claude (Anthropic), following the design of Lab Tutorial 1.

import java.util.Iterator;
import java.util.Scanner;

public class Main {
    void main() throws Exception {
        Scanner sc = new Scanner(System.in);
        int height = sc.nextInt();
        int tubes = sc.nextInt();
        sc.nextLine();
        StringBuilder configuration = new StringBuilder();
        for (int row = 0; row < height; row++) {
            String line = sc.nextLine();
            if (line.split(" ", -1).length != tubes)
                throw new IllegalArgumentException();
            configuration.append(line).append('\n');
        }
        BestFirst s = new BestFirst();
        Iterator<BestFirst.State> it =
            s.solve(new BallSortLayout(configuration.toString()), null);
        if (it == null) IO.println("no solution found");
        else while (it.hasNext()) {
            BestFirst.State i = it.next();
            if (!it.hasNext()) IO.println((int) i.getG());
        }
        sc.close();
    }
}
