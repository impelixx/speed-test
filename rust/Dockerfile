FROM rust:latest

WORKDIR /usr/src/app
COPY . .

RUN cargo build --release

ENTRYPOINT ["/usr/src/app/target/release/app"]
