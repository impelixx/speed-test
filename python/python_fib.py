import time
import sys

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Ошибка: Аргумент должен быть целым числом.")
            sys.exit(1)
    else:
        n = 40 # Значение по умолчанию, если аргумент не передан
    
    start_time = time.time()
    result = fibonacci(n)
    end_time = time.time()
    print(f"Python Fibonacci({n}): {result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")