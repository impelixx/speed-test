FROM gcc:latest

WORKDIR /app

COPY cpp_sieve.cpp .

RUN g++ -o cpp_sieve cpp_sieve.cpp -O2 -std=c++11

ENTRYPOINT ["./cpp_sieve"]