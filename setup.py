import io
from setuptools import setup


def get_readme():
    with io.open('README.rst') as f:
        return f.read()


install_required = [
    'atomicwrites',
    'attrs',
    'certifi',
    'chardet',
    'entrypoints',
    'idna',
    'mccabe',
    'more-itertools',
    'ortools',
    'pluggy',
    'protobuf',
    'py',
    'pycodestyle',
    'six'
]

setup(name='vroutes',
      version='0.1',
      description='A simple implementation of vehicle routing problems using Google OR-tools',
      long_description=get_readme(),
      url='http://github.com/rizkiaditya24/vroutes',
      author='Rizki Aditya',
      author_email='mradityanod@gmail.com',
      license='BSD',
      install_requires=install_required,
      packages=['vroutes'],
      zip_safe=False)
