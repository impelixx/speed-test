FROM gcc:latest AS gcc_build
WORKDIR /app
COPY cpp_sieve.cpp .
RUN g++ -O3 -o cpp_sieve_gcc cpp_sieve.cpp

FROM clang:latest AS clang_build
WORKDIR /app
COPY cpp_sieve.cpp .
RUN clang++ -O3 -o cpp_sieve_clang cpp_sieve.cpp

# Default to GCC build
FROM gcc_build
ENV CPP_COMPILER_NAME="C++-GCC"
ENTRYPOINT ["./cpp_sieve_gcc"]
