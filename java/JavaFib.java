public class JavaFib {

    public static long fibonacci(int n) {
        if (n <= 0) {
            return 0;
        } else if (n == 1) {
            return 1;
        } else {
            long a = 0;
            long b = 1;
            for (int i = 2; i <= n; i++) {
                long temp = b;
                b = a + b;
                a = temp;
            }
            return b;
        }
    }

    public static void main(String[] args) {
        int n;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                System.err.println("Ошибка: Аргумент должен быть целым числом.");
                return;
            }
        } else {
            n = 40; // Значение по умолчанию
        }
        
        long startTime = System.nanoTime();
        long result = fibonacci(n);
        long endTime = System.nanoTime();
        long timeTaken = endTime - startTime;

        System.out.println("Java Fibonacci(" + n + "): " + result);
        System.out.printf("Time taken: %.6f seconds%n", timeTaken / 1_000_000_000.0);
    }
}