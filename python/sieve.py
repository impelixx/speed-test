import time
import sys
import json
import os

def sieve_of_eratosthenes(limit):
    primes = []
    is_prime = [True] * (limit + 1)
    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p*p, limit + 1, p):
                is_prime[multiple] = False
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
    return primes

if __name__ == "__main__":
    # Определяем имя интерпретатора из переменной окружения или используем значение по умолчанию
    interpreter_identifier = os.environ.get("PYTHON_INTERPRETER_NAME", "Python-CPython")

    if len(sys.argv) > 1:
        try:
            n_limit = int(sys.argv[1])
            if n_limit < 0:
                print(json.dumps({
                    "language": interpreter_identifier,
                    "limit_arg": sys.argv[1],
                    "error": "Аргумент должен быть положительным целым числом."
                }), file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print(json.dumps({
                "language": interpreter_identifier,
                "limit_arg": sys.argv[1],
                "error": "Аргумент должен быть целым числом."
            }), file=sys.stderr)
            sys.exit(1)
    else:
        n_limit = 2000000

    start_time = time.perf_counter() # Используем perf_counter для большей точности
    prime_numbers = sieve_of_eratosthenes(n_limit)
    end_time = time.perf_counter()

    count = len(prime_numbers)
    time_taken = end_time - start_time

    result = {
        "language": interpreter_identifier,
        "limit": n_limit,
        "primes_count": count,
        "time_seconds": "{:.9f}".format(time_taken) # Форматируем в строку с 9 знаками
    }
    print(json.dumps(result))
