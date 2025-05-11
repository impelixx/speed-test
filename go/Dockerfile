FROM golang:1.20-alpine

WORKDIR /app

COPY go_sieve.go .

RUN go build -o go_sieve go_sieve.go

ENTRYPOINT ["./go_sieve"]