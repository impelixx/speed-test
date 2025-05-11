import 'dart:io';
import 'dart:math';
import 'dart:convert';

class Result {
  String language;
  int limit;
  int primes_count;
  String time_seconds;

  Result(this.language, this.limit, this.primes_count, this.time_seconds);

  Map<String, dynamic> toJson() => {
        'language': language,
        'limit': limit,
        'primes_count': primes_count,
        'time_seconds': time_seconds,
      };
}

List<int> sieveOfEratosthenes(int limit) {
  if (limit < 2) return [];
  var isPrime = List<bool>.filled(limit + 1, true);
  isPrime[0] = false;
  isPrime[1] = false;
  for (var p = 2; p * p <= limit; p++) {
    if (isPrime[p]) {
      for (var i = p * p; i <= limit; i += p) {
        isPrime[i] = false;
      }
    }
  }
  var primes = <int>[];
  for (var p = 2; p <= limit; p++) {
    if (isPrime[p]) {
      primes.add(p);
    }
  }
  return primes;
}

void main(List<String> arguments) {
  var limit = 2000000; // Default value

  if (arguments.isNotEmpty) {
    try {
      var newLimit = int.parse(arguments[0]);
      if (newLimit < 0) {
        stderr.writeln(jsonEncode({
          'language': 'Dart',
          'limit': newLimit,
          'error': 'Аргумент должен быть положительным целым числом.'
        }));
        exit(1);
      }
      limit = newLimit;
    } catch (e) {
      stderr.writeln(jsonEncode({
        'language': 'Dart',
        'limit_arg': arguments[0],
        'error': 'Аргумент должен быть целым числом.'
      }));
      exit(1);
    }
  }

  var stopwatch = Stopwatch()..start();
  var primeNumbers = sieveOfEratosthenes(limit);
  stopwatch.stop();
  var count = primeNumbers.length;
  var duration = stopwatch.elapsedMicroseconds / 1000000.0;

  var result = Result('Dart', limit, count, duration.toStringAsFixed(9));
  print(jsonEncode(result.toJson()));
}
