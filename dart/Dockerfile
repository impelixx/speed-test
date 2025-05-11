# Используем официальный образ Dart
FROM dart:stable

WORKDIR /app

# Create pubspec.yaml with proper YAML formatting
RUN echo 'name: sieve\n\
version: 1.0.0\n\
description: Sieve of Eratosthenes implementation\n\
environment:\n\
  sdk: ">=2.19.0 <3.0.0"\n\
dependencies:\n\
  json5: ^0.8.2\n' > pubspec.yaml

# Copy source file
COPY dart_sieve.dart .

# Get dependencies and compile
RUN dart pub get
RUN dart compile exe dart_sieve.dart -o dart_sieve

ENTRYPOINT ["./dart_sieve"]
