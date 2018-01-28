.PHONY: docs test

VIRTUALENV = $(shell which virtualenv)

help:
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  compile     runs the environments setup.py build install"
	@echo "  console     runs an interactive python console with current environment"
	@echo "  coverage    runs the tests and determines amount of code that is covered in the tests"
	@echo "  deps        install dependencies using pip"
	@echo "  install 		 installs the environment"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"
	@echo "  venv        returns the python environment being used"

clean:
	rm -rf *.egg-info/
	rm -rf .cache/
	rm .coverage || true
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -fr venv
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -name "*.pyc" -type f -print0 | xargs -0 /bin/rm -rf

compile:
	. venv/bin/activate; python setup.py build install

console:
	. venv/bin/activate; python

coverage:
	. venv/bin/activate; coverage run --source cybric setup.py test
	. venv/bin/activate; coverage html
	. venv/bin/activate; coverage report

deps:
	. venv/bin/activate; python -m pip install -r requirements.txt

docker_install: clean
	python setup.py install

install: clean venv deps
	. venv/bin/activate; python setup.py install

launch:
	. venv/bin/activate; python src/app.py

lint:
	. venv/bin/activate; pip install flake8==3.3.0
	. venv/bin/activate; python -m flake8 --ignore=F401,E501,E731 cybric/

test_local:
	. venv/bin/activate; pip install pytest==3.2.3 pytest-cov==2.5.1 responses==0.5.1 minimock==1.2.8 mock==2.0.0
	. venv/bin/activate; py.test --cov=cybric tests -r w --disable-pytest-warnings

test:
	. venv/bin/activate; python setup.py test

tox:
	. venv/bin/activate; pip install aiokafka==0.3.1 pytest==3.2.3 pytest-cov==2.5.1 responses==0.5.1 minimock==1.2.8 mock==2.0.0
	. venv/bin/activate; tox

venv:
	$(VIRTUALENV) -p python3.6 venv
