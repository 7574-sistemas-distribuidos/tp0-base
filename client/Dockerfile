FROM golang:1.14

ARG GIT_REMOTE
ARG CLIENT_PROGRAM_NAME 

RUN mkdir -p /build
WORKDIR /build/
COPY . .
RUN GOOS=linux go build -mod vendor -o bin/consumer ${GIT_REMOTE}/${CLIENT_PROGRAM_NAME}

FROM alpine:3.11
COPY --from=0 /build/bin/$CLIENT_PROGRAM_NAME /usr/local/sbin/$CLIENT_PROGRAM_NAME
ENTRYPOINT ["/bin/sh"]