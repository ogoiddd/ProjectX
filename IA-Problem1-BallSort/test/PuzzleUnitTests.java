import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PuzzleUnitTests {
    @Test
    public void testSample1() throws Exception {
        String input = "3 3\nR B E\nB B E\nR R E\n";
        StringWriter writer = new StringWriter();
        PrintWriter pw = new PrintWriter(writer);
        pw.println("R B E");
        pw.println("B B E");
        pw.println("R R E");
        pw.println();
        pw.println("R E E");
        pw.println("B B E");
        pw.println("R R B");
        pw.println();
        pw.println("R E E");
        pw.println("B E B");
        pw.println("R R B");
        pw.println();
        pw.println("E E E");
        pw.println("B R B");
        pw.println("R R B");
        pw.println();
        pw.println("E E B");
        pw.println("E R B");
        pw.println("R R B");
        pw.println();
        pw.println("E R B");
        pw.println("E R B");
        pw.println("E R B");
        pw.println();
        pw.println("5");
        pw.close();
        // JUnit expects the expected value first, then the actual value.
        assertEquals(writer.toString().replace("\r\n", "\n"), runMain(input));
    }

    @Test
    public void testSample2() throws Exception {
        String input = "3 4\nP R B E\nR B R E\nP B P E\n";
        StringWriter writer = new StringWriter();
        PrintWriter pw = new PrintWriter(writer);
        pw.println("P R B E");
        pw.println("R B R E");
        pw.println("P B P E");
        pw.println();
        pw.println("P E B E");
        pw.println("R B R E");
        pw.println("P B P R");
        pw.println();
        pw.println("P B E E");
        pw.println("R B R E");
        pw.println("P B P R");
        pw.println();
        pw.println("P B E E");
        pw.println("R B E R");
        pw.println("P B P R");
        pw.println();
        pw.println("E B E E");
        pw.println("R B P R");
        pw.println("P B P R");
        pw.println();
        pw.println("E B E R");
        pw.println("E B P R");
        pw.println("P B P R");
        pw.println();
        pw.println("E B P R");
        pw.println("E B P R");
        pw.println("E B P R");
        pw.println();
        pw.println("6");
        pw.close();
        // JUnit expects the expected value first, then the actual value.
        assertEquals(writer.toString().replace("\r\n", "\n"), runMain(input));
    }

    // Feed input to the supplied Main and capture its complete output.
    private String runMain(String input) throws Exception {
        InputStream previousIn = System.in;
        PrintStream previousOut = System.out;
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        PrintStream captured = new PrintStream(bytes, true, "UTF-8");
        try {
            System.setIn(new ByteArrayInputStream(input.getBytes(StandardCharsets.UTF_8)));
            System.setOut(captured);
            Main.main(new String[0]);
        } finally {
            System.setIn(previousIn);
            System.setOut(previousOut);
            captured.close();
        }
        return bytes.toString("UTF-8").replace("\r\n", "\n");
    }
}
