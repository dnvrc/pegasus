.PHONY: docs test

VIRTUALENV = $(shell which virtualenv)
PYTHONEXEC = $(shell which python3.6)
DOCKER_VOL = '/var/run/docker.sock:/var/run/docker.sock'
PIMAGENAME = 'amanelis/crypto-anaylze:public'
DIMAGENAME = 'amanelis/crypto-anaylze:latest'

bandit:
	. venv/bin/activate; pip install bandit==1.0.1
	. venv/bin/activate; bandit -r src/

bitinfocharts:
	. venv/bin/activate; $(PYTHONEXEC) src/api/bitinfochart/__init__.py

clean:
	rm .coverage || true
	rm -rf .cache
	rm -rf .eggs
	rm -rf .tox
	rm -rf *.egg-info/
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -fr venv
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -name "*.pyc" -type f -print0 | xargs -0 /bin/rm -rf

compile:
	. venv/bin/activate; $(PYTHONEXEC) setup.py build install

console:
	. venv/bin/activate; $(PYTHONEXEC)

corr_0725:
	. venv/bin/activate; $(PYTHONEXEC) src/models/corr_0725/__init__.py

corr_0725_r:
	python setup.py build install
	python src/models/corr_0725/__init__.py

coverage:
	. venv/bin/activate; coverage run --source src setup.py test
	. venv/bin/activate; coverage html
	. venv/bin/activate; coverage report

deps:
	. venv/bin/activate; $(PYTHONEXEC) -m pip install -r requirements.txt

docker_install: clean
	python setup.py install

install: clean venv deps
	. venv/bin/activate; $(PYTHONEXEC) setup.py install

# DB Migration tasks -----------------------------------------------------------
current:
	alembic current

history:
	alembic history --verbose

migrate:
	alembic upgrade head

reset:
	alembic downgrade base

upgrade:
	alembic upgrade +1

rollback:
	alembic downgrade -1

schema:
	alembic upgrade head --sql > ./alembic/schema.sql
# DB Migration tasks -----------------------------------------------------------

lint:
	. venv/bin/activate; pip install flake8==3.3.0
	. venv/bin/activate; $(PYTHONEXEC) -m flake8 --ignore=F401,E501,E731 src/

test:
	. venv/bin/activate; $(PYTHONEXEC) setup.py test

tox:
	. venv/bin/activate; pip install aiokafka==0.3.1 pytest==3.2.3 pytest-cov==2.5.1 responses==0.5.1 minimock==1.2.8 mock==2.0.0
	. venv/bin/activate; tox

venv:
	$(VIRTUALENV) -p $(PYTHONEXEC) venv
