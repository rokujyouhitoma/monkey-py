PYTHON=python

all: clean isort yapf flake8 mypy test

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

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
