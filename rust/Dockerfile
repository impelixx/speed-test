FROM rust:1.70 as builder

WORKDIR /usr/src/app
COPY . .

RUN cargo build --release

FROM debian:buster-slim
COPY --from=builder /usr/src/app/target/release/rust_fib /usr/local/bin/app

ENTRYPOINT ["app"]