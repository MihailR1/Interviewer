ifneq (,$(wildcard .env))
$(info Found .env file.)
include .env
export
endif

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

style:
	flake8 .
types:
	mypy app --explicit-package-bases
tests:
	pytest --lf --v
sorts:
	isort app -rc
check:
	make -j3 style types tests
