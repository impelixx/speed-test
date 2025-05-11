use std::time::Instant;
use std::env;
use std::process;
use serde::{Serialize};
use serde_json;

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

#[derive(Serialize)]
struct Result {
    language: String,
    limit: usize,
    primes_count: usize,
    time_seconds: String, // Изменено с f64 на String
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let limit: usize;

    if args.len() > 1 {
        match args[1].parse::<usize>() {
            Ok(num) => limit = num,
            Err(_) => {
                let error_json = serde_json::json!({ "error": "Аргумент должен быть положительным целым числом." });
                eprintln!("{}", serde_json::to_string(&error_json).unwrap());
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

    let result = Result {
        language: "Rust".to_string(),
        limit,
        primes_count: count,
        // Время форматируется в строку с 9 знаками после запятой
        time_seconds: format!("{:.9}", duration.as_secs_f64()),
    };

    match serde_json::to_string(&result) {
        Ok(json_string) => println!("{}", json_string),
        Err(e) => {
            // Should not happen with this struct
            let error_json = serde_json::json!({ "error": format!("Error serializing JSON: {}", e) });
            eprintln!("{}", serde_json::to_string(&error_json).unwrap());
            process::exit(1);
        }
    }
}