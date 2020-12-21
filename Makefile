.PHONY: start stop build test

image := 192.168.1.10:4000/builder
commit := $(shell git rev-parse --short HEAD)
branch:= $(shell git rev-parse --abbrev-ref HEAD)

build:
	docker build --build-arg COMMIT=$(commit) \
	-t $(image):$(commit) \
	-t $(image):$(branch) \
	-t $(image):latest .
	docker push $(image):$(commit)
	docker push $(image):$(branch)
	docker push $(image):latest

start:
	docker run -v $(PWD):/code --rm --name builder -p 5000:5000 -p 6000:6000 alexcreek/builder:latest

stop:
	docker kill builder

test:
	pipenv run pytest
