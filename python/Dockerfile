FROM python:3.10-slim AS cpython_base

WORKDIR /app
COPY sieve.py .
RUN pip install --no-cache-dir json5

FROM pypy:3.10-slim AS pypy_base
WORKDIR /app
COPY sieve.py .
RUN pip install --no-cache-dir json5

# Build stage for CPython
FROM cpython_base AS cpython
ENTRYPOINT ["python", "sieve.py"]

# Build stage for PyPy
FROM pypy_base AS pypy
ENTRYPOINT ["pypy", "sieve.py"]

# Default to CPython
FROM cpython