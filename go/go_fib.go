package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func fibonacci(n int) uint64 {
	if n <= 0 {
		return 0
	} else if n == 1 {
		return 1
	}

	var a, b uint64 = 0, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}

func main() {
	var n int
	if len(os.Args) > 1 {
		var err error
		n, err = strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Fprintln(os.Stderr, "Ошибка: Аргумент должен быть целым числом.")
			os.Exit(1)
		}
	} else {
		n = 40 // Значение по умолчанию
	}

	startTime := time.Now()
	result := fibonacci(n)
	duration := time.Since(startTime)

	fmt.Printf("Go Fibonacci(%d): %d\n", n, result)
	fmt.Printf("Time taken: %f seconds\n", duration.Seconds())
}
