package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func sieveOfEratosthenes(limit int) []int {
	isPrime := make([]bool, limit+1)
	for i := range isPrime {
		isPrime[i] = true
	}
	if limit >= 0 {
		isPrime[0] = false
	}
	if limit >= 1 {
		isPrime[1] = false
	}

	for p := 2; float64(p*p) <= float64(limit); p++ {
		if isPrime[p] {
			for i := p * p; i <= limit; i += p {
				isPrime[i] = false
			}
		}
	}

	primes := []int{}
	for p := 2; p <= limit; p++ {
		if isPrime[p] {
			primes = append(primes, p)
		}
	}
	return primes
}

func main() {
	var limit int
	if len(os.Args) > 1 {
		var err error
		limit, err = strconv.Atoi(os.Args[1])
		if err != nil || limit < 0 {
			fmt.Fprintln(os.Stderr, "Ошибка: Аргумент должен быть положительным целым числом.")
			os.Exit(1)
		}
	} else {
		limit = 2000000 // Значение по умолчанию
	}

	startTime := time.Now()
	primeNumbers := sieveOfEratosthenes(limit)
	duration := time.Since(startTime)
	count := len(primeNumbers)

	fmt.Printf("Go Sieve up to %d: %d primes\n", limit, count)
	fmt.Printf("Time taken: %f seconds\n", duration.Seconds())
}
