use std::time::Instant;
use std::env;
use std::process;

fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    let mut primes = Vec::new();
    let mut is_prime = vec![true; limit + 1];
    if limit >= 0 {
        if is_prime.len() > 0 { is_prime[0] = false; }
    }
    if limit >= 1 {
         if is_prime.len() > 1 { is_prime[1] = false; }
    }

    for p in 2..=(limit as f64).sqrt() as usize {
        if is_prime[p] {
            for i in (p * p..=limit).step_by(p) {
                is_prime[i] = false;
            }
        }
    }

    for p in 2..=limit {
        if is_prime[p] {
            primes.push(p);
        }
    }
    primes
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let limit: usize;

    if args.len() > 1 {
        match args[1].parse::<usize>() {
            Ok(num) => limit = num,
            Err(_) => {
                eprintln!("Ошибка: Аргумент должен быть положительным целым числом.");
                process::exit(1);
            }
        }
    } else {
        limit = 2000000; // Значение по умолчанию
    }

    let start_time = Instant::now();
    let prime_numbers = sieve_of_eratosthenes(limit);
    let duration = start_time.elapsed();
    let count = prime_numbers.len();

    println!("Rust Sieve up to {}: {} primes", limit, count);
    println!("Time taken: {:.6} seconds", duration.as_secs_f64());
}