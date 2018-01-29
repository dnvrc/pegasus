from setuptools import find_packages, setup

setup(
    name='crypto-analyze',
    description='Coin data analysis and Correlation models.',
    author='Alex Manelis',
    version='1.0.1',
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    url='https://github.com/amanelis/crypto-analyze',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'dotmap==1.2.20',
        'jupyter==1.0.0',
        'ipython==6.1.0',
        'plotly==2.3.0',
        'python-json-logger==0.1.7',
        'quandl==3.3.0',
        'requests[security]==2.18.4',
        'restapi-logging-handler==0.2.2',
        'tox==2.6.0',
        'urllib3==1.22',
    ],
    tests_require=[
        'coverage==4.4.1',
        'flake8==3.3.0',
        'minimock==1.2.8',
        'mock==2.0.0',
        'pytest==3.2.1',
        'responses==0.5.1',
        'tox==2.6.0',
    ],
    test_suite='tests',
)
