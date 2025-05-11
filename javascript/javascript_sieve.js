function sieveOfEratosthenes(limit) {
    const primes = [];
    const isPrime = new Array(limit + 1).fill(true);
    if (limit >= 0 && limit + 1 > 0) isPrime[0] = false;
    if (limit >= 1 && limit + 1 > 1) isPrime[1] = false;

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

// Определяем имя среды выполнения из переменной окружения или используем значение по умолчанию
const runtimeIdentifier = process.env.JS_RUNTIME_NAME || "JavaScript-Node";

if (nArg) {
    limit = parseInt(nArg, 10);
    if (isNaN(limit) || limit < 0) {
        console.error(JSON.stringify({
            language: runtimeIdentifier,
            limit_arg: nArg,
            error: "Аргумент должен быть положительным целым числом."
        }));
        process.exit(1);
    }
} else {
    limit = 2000000; // Значение по умолчанию
}

const startTime = performance.now(); // Используем performance.now() для лучшей переносимости
const primeNumbers = sieveOfEratosthenes(limit);
const endTime = performance.now();
const timeTakenMs = endTime - startTime;
const timeTakenSeconds = timeTakenMs / 1000.0;

const result = {
    language: runtimeIdentifier,
    limit: limit,
    primes_count: primeNumbers.length,
    time_seconds: timeTakenSeconds.toFixed(9) // Форматируем в строку с 9 знаками после запятой
};
console.log(JSON.stringify(result));
