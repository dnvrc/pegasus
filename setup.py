from setuptools import find_packages, setup

setup(
    name='pegasus',
    description='Coin data analysis and Correlation models.',
    author='Alex Manelis',
    version='1.0.1',
    platforms=['any'],
    url='https://github.com/amanelis/pegasus',
    license='proprietary',
    data_files = [('', ['LICENSE'])],
    classifiers=[
        'Topic :: Software Development :: Internal Tools',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    tests_require=[
    ],
    test_suite='tests',
)
