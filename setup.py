from setuptools import find_packages, setup

setup(
    name='crypto-analyze',
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    url='https://github.com/cybricio/python-cybric-bundle',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    tests_require=[
    ],
    test_suite='tests',
)
