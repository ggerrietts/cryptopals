
build:
	docker build -t cryptopals .

run:
	docker run --rm -v $(shell pwd):/usr/src/app cryptopals

ipython:
	docker run --rm -it -v $(shell pwd):/usr/src/app cryptopals ipython
