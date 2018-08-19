PYTHON=python

all: isort yapf flake8 mypy test

repl:
	@PYTHON main.py

test:
	@PYTHON -m unittest discover tests/

isort:
	isort -y

yapf:
	yapf -i -r .

flake8:
	flake8

mypy:
	mypy .
