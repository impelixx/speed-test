package main

import (
	"encoding/json"
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

// Result struct for JSON marshalling
type Result struct {
	Language    string `json:"language"`
	Limit       int    `json:"limit"`
	PrimesCount int    `json:"primes_count"`
	TimeSeconds string `json:"time_seconds"` // Изменено с float64 на string
}

func main() {
	var limit int
	if len(os.Args) > 1 {
		var err error
		limit, err = strconv.Atoi(os.Args[1])
		if err != nil || limit < 0 {
			jsonError, _ := json.Marshal(map[string]string{"error": "Аргумент должен быть положительным целым числом."})
			fmt.Fprintln(os.Stderr, string(jsonError))
			os.Exit(1)
		}
	} else {
		limit = 2000000 // Значение по умолчанию
	}

	startTime := time.Now()
	primeNumbers := sieveOfEratosthenes(limit)
	duration := time.Since(startTime)
	count := len(primeNumbers)

	result := Result{
		Language:    "Go",
		Limit:       limit,
		PrimesCount: count,
		// Время форматируется в строку с 9 знаками после запятой
		TimeSeconds: fmt.Sprintf("%.9f", duration.Seconds()),
	}

	jsonOutput, err := json.Marshal(result)
	if err != nil {
		// Should not happen with this struct
		fmt.Fprintln(os.Stderr, "Error marshalling JSON:", err)
		os.Exit(1)
	}
	fmt.Println(string(jsonOutput))
}
