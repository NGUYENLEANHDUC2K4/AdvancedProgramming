import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TestRunner {
    public static void main(String[] args) {
        System.out.println("Running Test Cases...");

        // Define test cases with fixed GROUND values and expected results
        List<TestCase> testCases = Arrays.asList(
            new TestCase(FixedTeamMaker.makeTeam1(), FixedTeamMaker.makeTeam2(), 100, 0.674),
            new TestCase(FixedTeamMaker.makeTeam3(), FixedTeamMaker.makeTeam4(), 250, 0.36825),
            new TestCase(FixedTeamMaker.makeTeam5(), FixedTeamMaker.makeTeam6(), 7, 0.1205)
        );

        for (int i = 0; i < testCases.size(); i++) {
            boolean testPassed = runTest(i + 1, testCases.get(i));
            System.out.println(testPassed ? "✅ Test Case " + (i + 1) + " Passed!" : "❌ Test Case " + (i + 1) + " Failed!");
        }
    }

    private static boolean runTest(int testNumber, TestCase testCase) {
        System.out.println("\nRunning Test Case " + testNumber + "...");

        // Capture console output
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outputStream));

        try {
            // Set the GROUND value manually before battle starts
            Battle.GROUND = testCase.ground;
            System.out.println("Forcing GROUND to: " + Battle.GROUND);

            // Run battle simulation
            Battle battle = new Battle(testCase.team1, testCase.team2);
            battle.combat();

            // Restore output
            System.setOut(originalOut);
            String actualOutput = outputStream.toString();
            Double actualPR = extractPRValue(actualOutput);

            // Compare results
            return validateTestResult(testCase.expectedPR, actualPR);
        } catch (Exception e) {
            System.setOut(originalOut);
            System.out.println("❌ Test Case " + testNumber + " Failed due to Exception!");
            e.printStackTrace();
            return false;
        }
    }

    // Extracts "pR = ..." value from the output
    private static Double extractPRValue(String output) {
        Matcher matcher = Pattern.compile("pR = ([0-9]*\\.?[0-9]+)").matcher(output);
        return matcher.find() ? Double.parseDouble(matcher.group(1)) : null;
    }

    // Validates and prints test results
    private static boolean validateTestResult(double expectedPR, Double actualPR) {
        if (actualPR != null && Math.abs(actualPR - expectedPR) < 1e-6) {
            return true;
        } else {
            System.out.println("❌ Expected: pR = " + expectedPR);
            System.out.println("❌ Actual: " + (actualPR != null ? "pR = " + actualPR : "No valid pR found"));
            return false;
        }
    }

    // Test case class for structured testing
    static class TestCase {
        Combatable[] team1;
        Combatable[] team2;
        int ground;
        double expectedPR;

        public TestCase(Combatable[] team1, Combatable[] team2, int ground, double expectedPR) {
            this.team1 = team1;
            this.team2 = team2;
            this.ground = ground;
            this.expectedPR = expectedPR;
        }
    }

    // Fixed TeamMaker for consistent test cases
    static class FixedTeamMaker {
        public static Combatable[] makeTeam1() { return new Combatable[]{ new Knight(600, 1) }; }
        public static Combatable[] makeTeam2() { return new Combatable[]{ new Warrior(650, 1) }; }
        public static Combatable[] makeTeam3() { return new Combatable[]{ new Knight(10, 1), new Paladin(10, 1) }; }
        public static Combatable[] makeTeam4() { return new Combatable[]{ new Warrior(650, 0), new DeathEater(new Complex(400, 300)) }; }
        public static Combatable[] makeTeam5() { return new Combatable[]{ new Knight(60, 0), new Paladin(70, 0), new Knight(80, 0) }; }
        public static Combatable[] makeTeam6() { return new Combatable[]{ new Warrior(600, 0), new DeathEater(new Complex(400, 300)), new Warrior(950, 1) }; }
    }
}
