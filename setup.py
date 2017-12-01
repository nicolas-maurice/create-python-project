"""
    Create-Python-Project
    ~~~~~~~~~~~~~~~~~~~~~

    Create-Python-Project is a CLI application to facilitate Python project management

    It is meant to be forked when starting a new Python project to inherit multiple DevOps functions.
"""

import os

from setuptools import setup


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Create-Python-Project',
    version='0.0.0',
    license=read('LICENSE.rst'),
    url='https://github.com/nicolas-maurice/create-python-project',
    author='Nicolas Maurice',
    author_email='nicolas.maurice.valera@gmail.com',
    description='Create-Python-Project is a CLI application to facilitate Python project management',
    packages=['create_python_project'],
    install_requires=[
        'click==6.3',
        'gitpython==2.1.7',
        'semver==2.7.9',
        'twine==1.9.1',
    ],
    extras_require={
        'dev': [
            'autoflake',
            'autopep8',
            'coverage',
            'flake8',
            'pytest>=3',
            'pytest-mock',
            'tox',
            'sphinx',
        ],
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
