#include <iostream>
#include <chrono>
#include <string> // Для std::stoi
#include <cstdlib> // Для std::exit

long long fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    long long a = 0;
    long long b = 1;
    for (int i = 2; i <= n; ++i) {
        long long temp = b;
        b = a + b;
        a = temp;
    }
    return b;
}

int main(int argc, char *argv[]) {
    int n;
    if (argc > 1) {
        try {
            n = std::stoi(argv[1]);
        } catch (const std::invalid_argument& ia) {
            std::cerr << "Ошибка: Аргумент должен быть целым числом." << std::endl;
            return 1;
        } catch (const std::out_of_range& oor) {
            std::cerr << "Ошибка: Аргумент вне допустимого диапазона." << std::endl;
            return 1;
        }
    } else {
        n = 40; // Значение по умолчанию
    }

    auto start = std::chrono::high_resolution_clock::now();
    long long result = fibonacci(n);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> diff = end - start;

    std::cout << "C++ Fibonacci(" << n << "): " << result << std::endl;
    std::cout << "Time taken: " << std::fixed << diff.count() << " seconds" << std::endl;

    return 0;
}