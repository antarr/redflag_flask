export PYTHONPATH := $(shell pwd)
check:
	coverage run --source=api -m unittest discover -s tests -p '*_test.py' -v && coverage report -m && coverage html
