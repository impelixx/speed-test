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
                    System.err.println("Ошибка: Аргумент должен быть положительным целым числом.");
                    return;
                }
            } catch (NumberFormatException e) {
                System.err.println("Ошибка: Аргумент должен быть целым числом.");
                return;
            }
        } else {
            limit = 2000000; // Значение по умолчанию
        }

        long startTime = System.nanoTime();
        List<Integer> primeNumbers = sieveOfEratosthenes(limit);
        long endTime = System.nanoTime();
        long timeTaken = endTime - startTime;
        int count = primeNumbers.size();

        System.out.println("Java Sieve up to " + limit + ": " + count + " primes");
        System.out.printf("Time taken: %.6f seconds%n", timeTaken / 1_000_000_000.0);
    }
}
