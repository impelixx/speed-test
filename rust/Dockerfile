FROM rust:1.70 as builder

WORKDIR /usr/src/app
COPY . .

RUN cargo build --release

FROM debian:buster-slim
# Исправлено имя исполняемого файла с rust_fib на app
COPY --from=builder /usr/src/app/target/release/app /usr/local/bin/app

ENTRYPOINT ["app"]