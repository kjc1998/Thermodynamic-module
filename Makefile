devinstall:
	pip install -e .[test]

test:
	python3 -m pytest -vv tests/

clean:
	find . -type d -iname __pycache__ | xargs rm -rf
	find . -type f -iname '*.pyc' | xargs rm -rf
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf **/*.egg-info

.PHONY: \
	black \
	clean \
	devinstall \
	devtest \
	help \
	version