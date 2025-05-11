import time
import sys
import json

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
    if len(sys.argv) > 1:
        try:
            n_limit = int(sys.argv[1])
            if n_limit < 0:
                print(json.dumps({"error": "Аргумент должен быть положительным целым числом."}))
                sys.exit(1)
        except ValueError:
            print(json.dumps({"error": "Аргумент должен быть целым числом."}))
            sys.exit(1)
    else:
        n_limit = 2000000 

    start_time = time.time()
    prime_numbers = sieve_of_eratosthenes(n_limit)
    end_time = time.time()
    
    count = len(prime_numbers)
    time_taken = end_time - start_time
    
    result = {
        "language": "Python",
        "limit": n_limit,
        "primes_count": count,
        "time_seconds": round(time_taken, 6)
    }
    print(json.dumps(result))
