.PHONY: help clean clean-build clean-pyc lint fmt test docs release dist run

help:
	@grep -E -h '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc ## Clean all

clean-build: ## Clean build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## Clean compiled python files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## Check PEP8 style with flake8, and rst with rst-lint
	flake8 watchman tests --ignore=E501
	rst-lint *.rst

fmt: ## Format python code with black
	black .

test: ## Run tests using GHA workflows with act
	act --job build

docs: ## Generate Sphinx HTML documentation, including API docs
	rm -f docs/watchman.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ watchman
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean lint test ## Package and upload a release
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

dist: clean lint test ## Package a release
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

run: ## Build and run sample project with docker
	docker build -t watchman .
	docker run -it -p 8000:8000 watchman
