FROM golang:latest

WORKDIR /app

COPY go_sieve.go .

RUN go build -o go_sieve go_sieve.go

ENTRYPOINT ["./go_sieve"]