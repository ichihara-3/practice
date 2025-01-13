FROM golang:bookworm AS builder
ENV CGO_ENABLED=0
WORKDIR /app
COPY . .
RUN go build -o helloapp

FROM scratch as final
COPY --from=builder /app/helloapp /app/helloapp
CMD ["/app/helloapp"]