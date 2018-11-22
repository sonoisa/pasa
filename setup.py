# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='pasa',
    packages=['pasa',
        'pasa.dict',
        'pasa.init',
        'pasa.parse',
        'pasa.result',
        'pasa.dict.category',
        'pasa.dict.cchart',
        'pasa.dict.compound_predicate',
        'pasa.dict.filter',
        'pasa.dict.frame',
        'pasa.dict.idiom',
        'pasa.dict.noun',
        'pasa.parse.analyzer',
        'pasa.parse.compound_predicate',
        'pasa.parse.feature',
        'pasa.parse.idiom',
        'pasa.parse.semantic'
    ],
    package_data = {
        'pasa': ['json/*.json']
    },
    description='Japanese Argument Structure Analyzer (ASA) for Python',
    long_description=readme,
    license='MIT',
    author='Isao Sonobe',
    author_email='sonoisa@gmail.com',
    url='https://github.com/sonoisa/pasa/',
    version='0.1.7',
    install_requires=[],
    dependency_links=['https://github.com/taku910/cabocha/tree/master/python/'],
    zip_safe=True
)
