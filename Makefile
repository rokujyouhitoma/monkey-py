PYTHON=python

repl:
	@PYTHON main.py

test:
	@PYTHON -m unittest discover tests/
