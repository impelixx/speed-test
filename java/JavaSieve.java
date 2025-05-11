import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class JavaSieve {

    public static List<Integer> sieveOfEratosthenes(int limit) {
        List<Integer> primes = new ArrayList<>();
        boolean[] isPrime = new boolean[limit + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;

        for (int p = 2; p * p <= limit; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= limit; i += p) {
                    isPrime[i] = false;
                }
            }
        }

        for (int p = 2; p <= limit; p++) {
            if (isPrime[p]) {
                primes.add(p);
            }
        }
        return primes;
    }

    public static void main(String[] args) {
        int limit;
        if (args.length > 0) {
            try {
                limit = Integer.parseInt(args[0]);
                if (limit < 0) {
                    System.out.println("{ \"error\": \"Аргумент должен быть положительным целым числом.\" }");
                    return;
                }
            } catch (NumberFormatException e) {
                System.out.println("{ \"error\": \"Аргумент должен быть целым числом.\" }");
                return;
            }
        } else {
            limit = 2000000; // Значение по умолчанию
        }

        long startTime = System.nanoTime();
        List<Integer> primeNumbers = sieveOfEratosthenes(limit);
        long endTime = System.nanoTime();
        double timeTaken = (endTime - startTime) / 1_000_000_000.0;
        int count = primeNumbers.size();
        String jsonResult = String.format(java.util.Locale.US,
                                        "{ \"language\": \"Java\", \"limit\": %d, \"primes_count\": %d, \"time_seconds\": %.6f }",
                                        limit, count, timeTaken);
        System.out.println(jsonResult);
    }
}
