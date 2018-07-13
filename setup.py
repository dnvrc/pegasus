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
    license='proprietary',
    data_files = [('', ['LICENSE'])],
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    tests_require=[
    ],
    test_suite='tests',
)
