FROM golang:1.14

RUN mkdir -p /build
WORKDIR /build/
COPY . .
# CGO_ENABLED must be disabled to run go binary in Alpine
RUN CGO_ENABLED=0 GOOS=linux go build -mod vendor -o bin/client github.com/7574-sistemas-distribuidos/docker-compose-init/client


FROM busybox:latest
COPY --from=0 /build/bin/client /client
ENTRYPOINT ["/bin/sh"]