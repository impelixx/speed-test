#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <string>
#include <cstdlib>
#include <iomanip>

std::vector<int> sieveOfEratosthenes(int limit) {
    std::vector<int> primes;
    std::vector<bool> is_prime(limit + 1, true);
    if (limit >= 0) is_prime[0] = false;
    if (limit >= 1) is_prime[1] = false;

    for (int p = 2; p * p <= limit; ++p) {
        if (is_prime[p]) {
            for (int i = p * p; i <= limit; i += p)
                is_prime[i] = false;
        }
    }

    for (int p = 2; p <= limit; ++p) {
        if (is_prime[p]) {
            primes.push_back(p);
        }
    }
    return primes;
}

int main(int argc, char *argv[]) {
    int limit;
    // Определяем имя компилятора из переменной окружения или используем значение по умолчанию
    const char* compiler_env = std::getenv("CPP_COMPILER_NAME");
    std::string compiler_identifier = compiler_env ? compiler_env : "C++-Unknown";

    if (argc > 1) {
        try {
            limit = std::stoi(argv[1]);
            if (limit < 0) {
                 std::cerr << "{ \"language\": \"" << compiler_identifier << "\", \"limit_arg\": " << argv[1] << ", \"error\": \"Аргумент должен быть положительным целым числом.\" }" << std::endl;
                 return 1;
            }
        } catch (const std::invalid_argument& ia) {
            std::cerr << "{ \"language\": \"" << compiler_identifier << "\", \"limit_arg\": \"" << argv[1] << "\", \"error\": \"Аргумент должен быть целым числом.\" }" << std::endl;
            return 1;
        } catch (const std::out_of_range& oor) {
            std::cerr << "{ \"language\": \"" << compiler_identifier << "\", \"limit_arg\": \"" << argv[1] << "\", \"error\": \"Аргумент вне допустимого диапазона.\" }" << std::endl;
            return 1;
        }
    } else {
        limit = 2000000; // Значение по умолчанию
    }

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<int> prime_numbers = sieveOfEratosthenes(limit);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> diff = end - start;
    int count = prime_numbers.size();
    double time_taken_seconds = diff.count();

    // Формируем JSON строку вручную
    std::cout << std::fixed << std::setprecision(9); // Увеличена точность до 9 знаков
    std::cout << "{ "
              << "\"language\": \"" << compiler_identifier << "\", "
              << "\"limit\": " << limit << ", "
              << "\"primes_count\": " << count << ", "
              << "\"time_seconds\": \"" << time_taken_seconds << "\"" // Время как строка
              << " }" << std::endl;

    return 0;
}
