FROM golang:1.14

ARG GIT_REMOTE
ARG CLIENT_PROGRAM_NAME 

RUN mkdir -p /build
WORKDIR /build/
COPY . .
# CGO_ENABLED must be disabled to run go binary in Alpine
RUN CGO_ENABLED=0 GOOS=linux go build -mod vendor -o bin/${CLIENT_PROGRAM_NAME} ${GIT_REMOTE}/${CLIENT_PROGRAM_NAME}

FROM busybox:latest
COPY --from=0 /build/bin/$CLIENT_PROGRAM_NAME /$CLIENT_PROGRAM_NAME
ENTRYPOINT ["/bin/sh"]