PYTHON=python

all: isort yapf

repl:
	@PYTHON main.py

test:
	@PYTHON -m unittest discover tests/

isort:
	isort -y

yapf:
	yapf -i -r .
