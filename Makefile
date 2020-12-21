.PHONY: start stop build test

commit := $(shell git rev-parse --short HEAD)

build:
	docker build --build-arg COMMIT=$(commit) -t 192.168.1.10:4000/remote:$(commit) .
	docker push 192.168.1.10:4000/remote:$(commit)

start:
	docker run -v $(PWD):/code --rm --name builder -p 5000:5000 -p 6000:6000 alexcreek/builder:latest

stop:
	docker kill builder

test:
	pipenv run pytest
