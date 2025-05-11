function fibonacci(n) {
    if (n <= 0) return 0;
    if (n === 1) return 1;

    let a = 0;
    let b = 1;
    for (let i = 2; i <= n; i++) {
        let temp = b;
        b = a + b;
        a = temp;
    }
    return b;
}

const nArg = process.argv[2];
let n;

if (nArg) {
    n = parseInt(nArg, 10);
    if (isNaN(n)) {
        console.error("Ошибка: Аргумент должен быть целым числом.");
        process.exit(1);
    }
} else {
    n = 40; // Значение по умолчанию
}

const startTime = process.hrtime();
const result = fibonacci(n);
const diff = process.hrtime(startTime);
const timeTaken = diff[0] * 1e9 + diff[1]; // nanoseconds

console.log(`JavaScript Fibonacci(${n}): ${result}`);
console.log(`Time taken: ${(timeTaken / 1e9).toFixed(6)} seconds`); // convert to seconds