FROM golang:1.18

WORKDIR /usr/src/app

COPY go.mod  ./
RUN go mod download && go mod verify

COPY . .
RUN go build -v -o /usr/loca/bin/app ./...

CMD ["app"]
