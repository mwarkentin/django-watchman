.PHONY: help clean clean-build clean-pyc lint test test-all coverage docs release dist run

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check PEP8 style with flake8, and rst with rst-lint"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package a release"
	@echo "run - build and run sample project with docker"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 watchman tests --ignore=E501
	rst-lint *.rst

test:
	python runtests.py

test-all:
	tox

coverage:
	coverage run --source watchman runtests.py
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/watchman.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ watchman
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean lint test
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload -r pypi

dist: clean lint test
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

run:
	docker build -t watchman .
	docker run -it -p 8000:8000 watchman
