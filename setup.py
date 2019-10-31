import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='factory',
    version='2.0.1',
    packages=find_packages(exclude=['core']),
    include_package_data=True,
    description='Django app to create and track different user defined tasks',
    long_description=README,
    url='https://www.github.com/tannerburns/factory',
    author='Tanner Burns',
    author_email='tjburns102@gmail.com',
    install_requires=[
        'django',
        'django-rest-framework',
        'django-filter',
        'psycopg2-binary'
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django-Rest-Framework',
        'Intended Audience :: Developers',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
