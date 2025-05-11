require 'json'
require 'time'

def sieve_of_eratosthenes(limit)
  is_prime = Array.new(limit + 1, true)
  is_prime[0] = false if limit >= 0
  is_prime[1] = false if limit >= 1

  (2..Math.sqrt(limit).to_i).each do |p|
    if is_prime[p]
      (p * p..limit).step(p) do |i|
        is_prime[i] = false
      end
    end
  end

  primes = []
  (2..limit).each do |p|
    primes << p if is_prime[p]
  end
  primes
end

limit = 2_000_000 # Значение по умолчанию

if ARGV.length > 0
  begin
    new_limit = Integer(ARGV[0])
    if new_limit < 0
      # Вывод ошибки в JSON формате, если предел отрицательный
      error_output = { language: "Ruby", limit: new_limit, error: "Аргумент должен быть положительным целым числом." }.to_json
      STDERR.puts error_output
      exit(1) # Выход с ошибкой
    end
    limit = new_limit
  rescue ArgumentError
    # Вывод ошибки в JSON формате, если аргумент не является числом
    error_output = { language: "Ruby", limit: ARGV[0], error: "Аргумент должен быть целым числом." }.to_json
    STDERR.puts error_output
    exit(1) # Выход с ошибкой
  end
end

start_time = Time.now
prime_numbers = sieve_of_eratosthenes(limit)
duration = Time.now - start_time
count = prime_numbers.length

result = {
  language: "Ruby",
  limit: limit,
  primes_count: count,
  time_seconds: "%.9f" % duration # Форматируем до 9 знаков после запятой
}

puts result.to_json
