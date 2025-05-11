\
function sieveOfEratosthenes(limit) {
    const primes = [];
    const isPrime = new Array(limit + 1).fill(true);
    isPrime[0] = isPrime[1] = false;

    for (let p = 2; p * p <= limit; p++) {
        if (isPrime[p]) {
            for (let i = p * p; i <= limit; i += p)
                isPrime[i] = false;
        }
    }

    for (let p = 2; p <= limit; p++) {
        if (isPrime[p]) {
            primes.push(p);
        }
    }
    return primes;
}

const nArg = process.argv[2];
let limit;

if (nArg) {
    limit = parseInt(nArg, 10);
    if (isNaN(limit) || limit < 0) {
        console.error("Ошибка: Аргумент должен быть положительным целым числом.");
        process.exit(1);
    }
} else {
    limit = 2000000; // Значение по умолчанию
}

const startTime = process.hrtime();
const primeNumbers = sieveOfEratosthenes(limit);
const diff = process.hrtime(startTime);
const timeTaken = diff[0] + diff[1] / 1e9; // seconds

console.log(`JavaScript Sieve up to ${limit}: ${primeNumbers.length} primes`);
console.log(`Time taken: ${timeTaken.toFixed(6)} seconds`);
