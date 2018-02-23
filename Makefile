test:
	pytest --cov=./ -v --cov-report=xml
	# py.test -n 8 --boxed --junitxml=report.xml
coverage:
	coverage xml

clean:
	rm -rf dist/
	rm -rf build/

build:
	# only build
	python setup.py sdist
	python setup.py bdist_wheel

publish: build
	twine upload dist/*
