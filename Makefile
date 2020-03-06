SHELL := /bin/bash

GIT_SHA := $(shell git rev-parse HEAD | cut -c 1-12)
VERSION := $(shell git describe --tags --dirty --always --abbrev=12)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
PWD := $(shell pwd)

GIT_REMOTE = github.com/Ezetowers/docker-compose-init
SERVER_PROGRAM_NAME = server
CLIENT_PROGRAM_NAME = client

SERVER_IMAGE_NAME = server
CLIENT_IMAGE_NAME = client

default: build

all:

deps:
	go mod tidy
	go mod vendor

build: deps
	GOOS=linux go build -o bin/client $(GIT_REMOTE)/$(CLIENT_PROGRAM_NAME)
.PHONY: build

build-darwin: deps
	GOOS=darwin go build -o bin/client $(GIT_REMOTE)/$(CLIENT_PROGRAM_NAME)
.PHONY: build-darwin

docker-image:
	docker build -f ./server/Dockerfile -t "$(SERVER_IMAGE_NAME):$(GIT_SHA)" .
	docker build --build-arg GIT_REMOTE=$(GIT_REMOTE) --build-arg CLIENT_PROGRAM_NAME=$(CLIENT_PROGRAM_NAME) -f ./client/Dockerfile -t "$(CLIENT_IMAGE_NAME):$(GIT_SHA)" .
.PHONY: docker-image

docker-compose-up:
	docker-compose -f docker-compose-dev.yaml up -d --build
.PHONY: docker-compose-up

docker-compose-down:
	docker-compose -f docker-compose-dev.yaml stop -t 1
	docker-compose -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	docker-compose -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs
