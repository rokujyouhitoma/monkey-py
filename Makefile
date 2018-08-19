PYTHON=python
ISORT=isort

all: isort

repl:
	@PYTHON main.py

test:
	@PYTHON -m unittest discover tests/

isort:
	@ISORT -y
