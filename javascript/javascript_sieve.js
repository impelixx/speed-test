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
        console.log(JSON.stringify({error: "Ошибка: Аргумент должен быть положительным целым числом."}));
        process.exit(1);
    }
} else {
    limit = 2000000;
}

const startTime = process.hrtime();
const primeNumbers = sieveOfEratosthenes(limit);
const diff = process.hrtime(startTime);
const timeTaken = diff[0] + diff[1] / 1e9;

const result = {
    language: "JavaScript",
    limit: limit,
    primes_count: primeNumbers.length,
    time_seconds: parseFloat(timeTaken.toFixed(6))
};
console.log(JSON.stringify(result));
